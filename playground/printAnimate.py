import time

def loading(t, staticString, sequence):
    # Animation sequence. Example: ['Loading |', 'Loading /', 'Loading -', 'Loading \\']
    for i in range(t):
        animation = staticString + sequence[ i % len(sequence)]
        # Clear line by adding the static string to the beggining of the line + some white space.
        print(staticString + ' ' * len(staticString), end='\r')
        print(animation, end='\r')
        time.sleep(1)
    print('Done!' + ' ' * len(staticString))

def waitMessage(t, staticString):
    for i in range(t, 0, -1):
        if i > 9:
            print(f'{staticString} {i} seconds.', end='\r')
            time.sleep(1)
        else:
            print(f'{staticString} {i} seconds.' + ' ' * 10, end='\r')
            time.sleep(1)

# Usage Examples
loading(10, 'This is a very long message for a loading screen', ['.', '..', '...'])
# waitMessage(20, 'Loading next sheet in')


