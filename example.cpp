// neural_network.cpp
// A complete neural network implementation in pure C++
// No libraries - just math and arrays
// Compile: g++ -std=c++17 -O3 neural_network.cpp -o neural_network

#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <iomanip>
#include <fstream>

using namespace std;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

// Sigmoid activation function: f(x) = 1 / (1 + e^(-x))
double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// Derivative of sigmoid: f'(x) = f(x) * (1 - f(x))
double sigmoid_derivative(double x) {
    double s = sigmoid(x);
    return s * (1.0 - s);
}

// Random number between -1 and 1
double random_weight() {
    static random_device rd;
    static mt19937 gen(rd());
    static uniform_real_distribution<> dis(-1.0, 1.0);
    return dis(gen);
}

// ============================================================================
// NEURAL NETWORK CLASS
// ============================================================================

class NeuralNetwork {
private:
    // Network architecture
    int input_size;
    int hidden_size;
    int output_size;
    
    // Weights and biases
    vector<vector<double>> weights_input_hidden;   // input -> hidden weights
    vector<double> bias_hidden;                     // hidden layer biases
    vector<vector<double>> weights_hidden_output;   // hidden -> output weights
    vector<double> bias_output;                     // output layer biases
    
    // Activations (values during forward pass)
    vector<double> hidden_layer;
    vector<double> output_layer;
    
    // Learning rate
    double learning_rate;

public:
    NeuralNetwork(int input_sz, int hidden_sz, int output_sz, double lr = 0.1) 
        : input_size(input_sz), 
          hidden_size(hidden_sz), 
          output_size(output_sz),
          learning_rate(lr) {
        
        // Initialize weights randomly
        // Input -> Hidden
        weights_input_hidden.resize(hidden_size, vector<double>(input_size));
        bias_hidden.resize(hidden_size);
        
        for (int i = 0; i < hidden_size; i++) {
            for (int j = 0; j < input_size; j++) {
                weights_input_hidden[i][j] = random_weight();
            }
            bias_hidden[i] = random_weight();
        }
        
        // Hidden -> Output
        weights_hidden_output.resize(output_size, vector<double>(hidden_size));
        bias_output.resize(output_size);
        
        for (int i = 0; i < output_size; i++) {
            for (int j = 0; j < hidden_size; j++) {
                weights_hidden_output[i][j] = random_weight();
            }
            bias_output[i] = random_weight();
        }
        
        // Initialize activation vectors
        hidden_layer.resize(hidden_size);
        output_layer.resize(output_size);
        
        cout << "Neural Network Created!" << endl;
        cout << "  Input neurons: " << input_size << endl;
        cout << "  Hidden neurons: " << hidden_size << endl;
        cout << "  Output neurons: " << output_size << endl;
        cout << "  Learning rate: " << learning_rate << endl << endl;
    }
    
    // ========================================================================
    // FORWARD PASS
    // ========================================================================
    
    vector<double> forward(const vector<double>& input) {
        // Input -> Hidden Layer
        for (int i = 0; i < hidden_size; i++) {
            double sum = bias_hidden[i];
            
            for (int j = 0; j < input_size; j++) {
                sum += input[j] * weights_input_hidden[i][j];
            }
            
            hidden_layer[i] = sigmoid(sum);
        }
        
        // Hidden -> Output Layer
        for (int i = 0; i < output_size; i++) {
            double sum = bias_output[i];
            
            for (int j = 0; j < hidden_size; j++) {
                sum += hidden_layer[j] * weights_hidden_output[i][j];
            }
            
            output_layer[i] = sigmoid(sum);
        }
        
        return output_layer;
    }
    
    // ========================================================================
    // BACKWARD PASS (Backpropagation)
    // ========================================================================
    
    void backward(const vector<double>& input, const vector<double>& target) {
        // Calculate output layer error
        vector<double> output_errors(output_size);
        vector<double> output_deltas(output_size);
        
        for (int i = 0; i < output_size; i++) {
            // Error = (target - output)
            output_errors[i] = target[i] - output_layer[i];
            
            // Delta = error * derivative
            output_deltas[i] = output_errors[i] * sigmoid_derivative(output_layer[i]);
        }
        
        // Calculate hidden layer error
        vector<double> hidden_errors(hidden_size, 0.0);
        vector<double> hidden_deltas(hidden_size);
        
        for (int i = 0; i < hidden_size; i++) {
            // Backpropagate error from output layer
            for (int j = 0; j < output_size; j++) {
                hidden_errors[i] += output_deltas[j] * weights_hidden_output[j][i];
            }
            
            // Delta = error * derivative
            hidden_deltas[i] = hidden_errors[i] * sigmoid_derivative(hidden_layer[i]);
        }
        
        // Update weights: Hidden -> Output
        for (int i = 0; i < output_size; i++) {
            for (int j = 0; j < hidden_size; j++) {
                // Weight update: w += learning_rate * delta * activation
                weights_hidden_output[i][j] += learning_rate * output_deltas[i] * hidden_layer[j];
            }
            // Update bias
            bias_output[i] += learning_rate * output_deltas[i];
        }
        
        // Update weights: Input -> Hidden
        for (int i = 0; i < hidden_size; i++) {
            for (int j = 0; j < input_size; j++) {
                weights_input_hidden[i][j] += learning_rate * hidden_deltas[i] * input[j];
            }
            // Update bias
            bias_hidden[i] += learning_rate * hidden_deltas[i];
        }
    }
    
    // ========================================================================
    // TRAINING
    // ========================================================================
    
    void train(const vector<vector<double>>& X, 
               const vector<vector<double>>& y, 
               int epochs) {
        
        cout << "Training started..." << endl;
        cout << string(50, '=') << endl;
        
        for (int epoch = 0; epoch < epochs; epoch++) {
            double total_loss = 0.0;
            
            // Train on each example
            for (size_t i = 0; i < X.size(); i++) {
                // Forward pass
                vector<double> prediction = forward(X[i]);
                
                // Calculate loss (MSE)
                for (size_t j = 0; j < prediction.size(); j++) {
                    double error = y[i][j] - prediction[j];
                    total_loss += error * error;
                }
                
                // Backward pass (learning)
                backward(X[i], y[i]);
            }
            
            // Average loss
            total_loss /= X.size();
            
            // Print progress
            if ((epoch + 1) % 1000 == 0) {
                cout << "Epoch " << setw(5) << (epoch + 1) 
                     << "/" << epochs 
                     << ", Loss: " << fixed << setprecision(6) << total_loss 
                     << endl;
            }
        }
        
        cout << string(50, '=') << endl;
        cout << "Training complete!" << endl << endl;
    }
    
    // ========================================================================
    // TESTING
    // ========================================================================
    
    void test(const vector<vector<double>>& X, const vector<vector<double>>& y) {
        cout << string(50, '=') << endl;
        cout << "Testing the network..." << endl;
        cout << string(50, '=') << endl;
        
        cout << "\nInput -> Predicted -> Actual" << endl;
        cout << string(35, '-') << endl;
        
        for (size_t i = 0; i < X.size(); i++) {
            vector<double> prediction = forward(X[i]);
            
            cout << "[";
            for (size_t j = 0; j < X[i].size(); j++) {
                cout << X[i][j];
                if (j < X[i].size() - 1) cout << ", ";
            }
            cout << "] -> ";
            
            cout << fixed << setprecision(4) << prediction[0] 
                 << " (" << round(prediction[0]) << ") -> "
                 << y[i][0];
            
            bool correct = (round(prediction[0]) == y[i][0]);
            cout << (correct ? " ✓" : " ✗") << endl;
        }
    }
    
    // ========================================================================
    // SAVE/LOAD WEIGHTS
    // ========================================================================
    
    void save_weights(const string& filename) {
        ofstream file(filename);
        
        // Save input->hidden weights
        for (const auto& row : weights_input_hidden) {
            for (double w : row) {
                file << w << " ";
            }
            file << "\n";
        }
        
        // Save hidden biases
        for (double b : bias_hidden) {
            file << b << " ";
        }
        file << "\n";
        
        // Save hidden->output weights
        for (const auto& row : weights_hidden_output) {
            for (double w : row) {
                file << w << " ";
            }
            file << "\n";
        }
        
        // Save output biases
        for (double b : bias_output) {
            file << b << " ";
        }
        
        file.close();
        cout << "💾 Weights saved to " << filename << endl;
    }
};

// ============================================================================
// MAIN PROGRAM
// ============================================================================

int main() {
    cout << "🧠 Building a Neural Network from Scratch in C++!" << endl;
    cout << "Task: Learn the XOR function\n" << endl;
    
    // XOR dataset
    vector<vector<double>> X = {
        {0.0, 0.0},
        {0.0, 1.0},
        {1.0, 0.0},
        {1.0, 1.0}
    };
    
    vector<vector<double>> y = {
        {0.0},
        {1.0},
        {1.0},
        {0.0}
    };
    
    cout << "Dataset created:" << endl;
    cout << "  Training examples: " << X.size() << endl;
    cout << "  Input features: " << X[0].size() << endl;
    cout << "  Output features: " << y[0].size() << endl << endl;
    
    // Create neural network
    NeuralNetwork nn(2, 4, 1, 0.5);
    
    // Train
    nn.train(X, y, 10000);
    
    // Test
    nn.test(X, y);
    
    // Save weights
    nn.save_weights("xor_weights.txt");
    
    cout << "\n✨ All done! The network learned XOR from scratch!" << endl;
    
    return 0;
}