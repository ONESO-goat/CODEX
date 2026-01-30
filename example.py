# neural_network_from_scratch.py
# A complete neural network trained from scratch using PyTorch

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class SimpleNeuralNetwork(nn.Module):
    """
    A simple 2-layer neural network
    Architecture: Input(2) -> Hidden(4) -> Output(1)
    """
    
    def __init__(self, input_size=2, hidden_size=4, output_size=1):
        super(SimpleNeuralNetwork, self).__init__()
        
        # Layer 1: Input to Hidden
        self.hidden = nn.Linear(input_size, hidden_size)
        
        # Layer 2: Hidden to Output
        self.output = nn.Linear(hidden_size, output_size)
        
        # Activation function
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        """
        Forward pass through the network
        
        x -> hidden layer -> activation -> output layer -> activation
        """
        # Pass through hidden layer
        hidden_output = self.hidden(x)
        
        # Apply activation (sigmoid)
        hidden_activated = self.sigmoid(hidden_output)
        
        # Pass through output layer
        final_output = self.output(hidden_activated)
        
        # Apply final activation
        result = self.sigmoid(final_output)
        
        return result


def create_xor_dataset():
    """
    Create XOR dataset
    XOR is a classic problem that's not linearly separable
    
    Truth table:
    0 XOR 0 = 0
    0 XOR 1 = 1
    1 XOR 0 = 1
    1 XOR 1 = 0
    """
    # Input data
    X = torch.tensor([
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ], dtype=torch.float32)
    
    # Expected outputs
    y = torch.tensor([
        [0.0],
        [1.0],
        [1.0],
        [0.0]
    ], dtype=torch.float32)
    
    return X, y


def train_network(model, X, y, epochs=10000, learning_rate=0.1):
    """
    Train the neural network
    
    This is where the magic happens - the network learns!
    """
    # Loss function (how wrong are we?)
    criterion = nn.MSELoss()  # Mean Squared Error
    
    # Optimizer (how do we improve?)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    
    # Track loss over time
    loss_history = []
    
    print("Training started...")
    print("=" * 50)
    
    for epoch in range(epochs):
        # Forward pass: compute predictions
        predictions = model(X)
        
        # Compute loss (how wrong are we?)
        loss = criterion(predictions, y)
        
        # Backward pass: compute gradients
        optimizer.zero_grad()  # Clear old gradients
        loss.backward()        # Calculate new gradients
        
        # Update weights
        optimizer.step()
        
        # Record loss
        loss_history.append(loss.item())
        
        # Print progress every 1000 epochs
        if (epoch + 1) % 1000 == 0:
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.6f}")
    
    print("=" * 50)
    print("Training complete!")
    
    return loss_history


def test_network(model, X, y):
    """
    Test the trained network
    """
    print("\n" + "=" * 50)
    print("Testing the network...")
    print("=" * 50)
    
    with torch.no_grad():  # Don't track gradients during testing
        predictions = model(X)
        
        print("\nInput -> Predicted -> Actual")
        print("-" * 35)
        
        for i in range(len(X)):
            input_vals = X[i].numpy()
            pred = predictions[i].item()
            actual = y[i].item()
            
            # Round prediction to 0 or 1
            pred_rounded = round(pred)
            
            correct = "✓" if pred_rounded == actual else "✗"
            
            print(f"{input_vals} -> {pred:.4f} ({pred_rounded}) -> {actual} {correct}")


def visualize_training(loss_history):
    """
    Plot the training loss over time
    """
    plt.figure(figsize=(10, 6))
    plt.plot(loss_history)
    plt.title('Training Loss Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale to see convergence better
    plt.tight_layout()
    plt.savefig('training_loss.png', dpi=150)
    print("\n📊 Training graph saved as 'training_loss.png'")


def inspect_network(model):
    """
    Look inside the trained network
    """
    print("\n" + "=" * 50)
    print("Network Architecture")
    print("=" * 50)
    print(model)
    
    print("\n" + "=" * 50)
    print("Learned Weights")
    print("=" * 50)
    
    for name, param in model.named_parameters():
        print(f"\n{name}:")
        print(param.data)


def main():
    """
    Main training pipeline
    """
    print("🧠 Building a Neural Network from Scratch!")
    print("Task: Learn the XOR function\n")
    
    # 1. Create the dataset
    X, y = create_xor_dataset()
    print("Dataset created:")
    print(f"  Inputs: {X.shape}")
    print(f"  Outputs: {y.shape}\n")
    
    # 2. Create the model
    model = SimpleNeuralNetwork(input_size=2, hidden_size=4, output_size=1)
    print("Model created:")
    print(f"  Input layer: 2 neurons")
    print(f"  Hidden layer: 4 neurons")
    print(f"  Output layer: 1 neuron\n")
    
    # 3. Train the model
    loss_history = train_network(
        model, 
        X, 
        y, 
        epochs=10000, 
        learning_rate=0.1
    )
    
    # 4. Test the model
    test_network(model, X, y)
    
    # 5. Visualize training
    visualize_training(loss_history)
    
    # 6. Inspect the network
    inspect_network(model)
    
    # 7. Save the model
    torch.save(model.state_dict(), 'xor_network.pth')
    print("\n💾 Model saved as 'xor_network.pth'")
    
    print("\n✨ All done! The network learned XOR from scratch!")


if __name__ == "__main__":
    while True:
        main()