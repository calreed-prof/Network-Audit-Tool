import itertools
import sys
import time
import threading

# Create a cycle of the loading symbols
loading_symbols = itertools.cycle(['.  ', '.. ', '...'])

def show_loading_animation():
    while not done:
        sys.stdout.write('\rFinding the best server' + next(loading_symbols))
        sys.stdout.flush()
        time.sleep(0.5)

# This flag will stop the loading animation once the server is found
done = False

# Start the loading animation in a separate thread
loading_thread = threading.Thread(target=show_loading_animation)
loading_thread.start()

# Simulate finding the best server (replace this with your actual logic)
time.sleep(5)  # Simulating delay for demonstration purposes
best_server = {'name': 'New York, NY', 'country': 'United States'}  # Example server data

# Stop the loading animation
done = True
loading_thread.join()

# Clear the loading line before printing the best server details
sys.stdout.write('\r' + ' ' * 50 + '\r')
sys.stdout.flush()

# Print the best server details
print(f"Best Server Found: {best_server['name']} in {best_server['country']}")
