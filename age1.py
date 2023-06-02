from ansible.errors import AnsibleError
import subprocess
import base64
import time
import os

AGEBIN = "age"

# age1, (C)May 2023 by Jan-Piet Mens <jp@mens.de>
# An Ansible filter to encrypt and decrypt data using https://age-encryption.org,
# inspired by a question by Christoph V.

def age_decrypt(encrypted, identity="ansible.key"):
    """
    encrypted is either age armour-encrypted or it's age encrypted and then
    base64-encoded.
    identity is an age secret key or keys
    """

    if identity is None:
        raise AnsibleError('No identity provided')
    if not os.access(identity, os.R_OK):
        raise AnsibleError('identity {0} is not readable'.format(identity))
    
    argv = [AGEBIN, "--decrypt", "-i", identity]
    p = subprocess.Popen(argv, stdout = subprocess.PIPE, stdin = subprocess.PIPE)

    if encrypted.startswith("-----BEGIN AGE ENCRYPTED"):
        p.stdin.write(encrypted.lstrip().encode())
    else:
        p.stdin.write(base64.b64decode(encrypted.lstrip().rstrip()))

    p.stdin.close()

    text = p.stdout.read().rstrip()
    p.stdout.close()

    while p.poll() is None:
        time.sleep(0.5)

    rc = p.returncode
    if rc != 0:
        raise AnsibleError('failed to decrypt with identity {0}: rc={1}'.format(identity, rc))
    return text

def age_encrypt(plain, recipient, armored=False):
    """
    encrypt the plain text to recipient with age, emitting binary
    or ASCII armor if armored is true.
    """
    argv = [AGEBIN, "--encrypt", "-r", recipient]

    if armored:
        argv.append("--armor")
    p = subprocess.Popen(argv, stdout = subprocess.PIPE, stdin = subprocess.PIPE)

    p.stdin.write(plain.encode())
    p.stdin.close()

    text = p.stdout.read().rstrip()
    p.stdout.close()

    while p.poll() is None:
        time.sleep(0.5)

    rc = p.returncode
    if rc != 0:
        raise AnsibleError('failed to encrypt with supplied recipient: rc={1}'.format(rc))
    return text

class FilterModule(object):
    def filters(self):
        return {
            'age_d'       : age_decrypt,
            'age_decrypt' : age_decrypt,
            'age_e'       : age_encrypt,
            'age_encrypt' : age_encrypt,
        }
