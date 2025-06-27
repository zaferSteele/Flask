# This function connects to a network device over SSH using pexpect,
# runs the "show version" command, captures the output, and returns it
# along with the device name. It handles SSH prompts and password input.

import pexpect

def show_version(device, prompt, ip, username, password):
    device_prompt = prompt

    # Start an SSH session by spawning an SSH process
    # This is like typing: ssh username@ip in a terminal
    child = pexpect.spawn(f'ssh {username}@{ip}', encoding='utf-8', timeout=20)
    
    # If you want to see the interaction for debugging, you can uncomment the line below
    # child.logfile = sys.stdout

    # When connecting to a device for the first time, SSH may ask if you're sure you want to connect
    # This checks if we get that "yes/no" prompt, or if it directly asks for a password
    i = child.expect([r'yes/no', r'Password:', r'password:', pexpect.EOF, pexpect.TIMEOUT])
    
    if i == 0:
        # If it asks "Are you sure you want to continue connecting (yes/no)?"
        child.sendline('yes')
        # Then wait for the password prompt and send the password
        child.expect([r'Password:', r'password:'])
        child.sendline(password)
    elif i in [1, 2]:
        # If it directly asks for a password, just send it
        child.sendline(password)
    else:
        # If something unexpected happens, raise an error
        raise Exception("SSH connection failed or timed out.")

    # Wait until we see the device's command prompt (so we know we're logged in)
    child.expect(device_prompt)
    
    # Send the command to show the version info (filtered for lines containing 'V')
    child.sendline('show version | i V')
    # Wait again for the command prompt so we know the output is complete
    child.expect(device_prompt)
    # Save the output from the command
    result = child.before

    # Send the exit command to log out
    child.sendline('exit')
    # Wait for the session to fully close
    child.expect(pexpect.EOF)

    # Return the device name and the output from the 'show version' command
    return device, result