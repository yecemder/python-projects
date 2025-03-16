import io
from time import sleep

# Create a StringIO buffer
buffer = io.StringIO()

# Print to the buffer
print("Hello, World!", file=buffer)
sleep(1)
print("This is a new line.", file=buffer)
print("Another line here.", file=buffer)

# Get the contents of the buffer
contents = buffer.getvalue()

# Close the buffer
buffer.close()

# Print the buffer contents
print("Buffer Contents:")
print(contents)
