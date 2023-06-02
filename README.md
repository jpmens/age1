## age1 filter for Ansible

### input

```yaml
- hosts: alic3
  vars:
      recipient: "age19q8pzgaxq2uynsrp3dluxv5apxmqym2pyldwpkp4s30qf4vfzqrsvvjzjv"
  tasks:

    - name: Encrypt to age with base64 encoding ..
      set_fact:
          secret: "{{ 'Moo 🐄' | age_e(recipient) | b64encode }}"
          armored: "{{ 'more moo 🐮' | age_e(recipient, true) }}"

    - name: .. and decrypt using age_d
      debug:
         msg: "{{ secret | age_d }}"

    - name: .. and decrypt the armored value using age_d
      debug:
         msg: "{{ armored | age_d }}"

    - name: Decrypt the age-encrypted and base64-encoded pangram
      debug:
         msg: "{{ ansible_local.pangram.p1.short | age_d }} liquor jugs"

    - name: Decrypt the age-encrypted and ASCII-armoured 2nd pangram
      debug:
         msg: "{{ ansible_local.other.armored | age_d('age.d/cow.key') }}"

    - name: Use age command to encrypt the current date string ...
      shell:
         cmd: "age -e -a -r {{ recipient }} <(date)"
         executable: /bin/bash  # yuck
      register: c

    - name: ... and decrypt it using our filter
      debug:
         msg: "{{ c.stdout | age_d }}"

```

### output

```
PLAY [alice] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [alice]

TASK [Encrypt to age with base64 encoding ..] **********************************
ok: [alice]

TASK [.. and decrypt using age_d] **********************************************
ok: [alice] => {
    "msg": "Moo 🐄"
}

TASK [.. and decrypt the armored value using age_d] ****************************
ok: [alice] => {
    "msg": "more moo 🐮"
}

TASK [Decrypt the age-encrypted and base64-encoded pangram] ********************
ok: [alice] => {
    "msg": "Pack my box with five dozen liquor jugs"
}

TASK [Decrypt the age-encrypted and ASCII-armoured 2nd pangram] ****************
ok: [alice] => {
    "msg": "The quick brown fox"
}

TASK [Use age command to encrypt the current date string ...] ******************
changed: [alice]

TASK [... and decrypt it using our filter] *************************************
ok: [alice] => {
    "msg": "Fri Jun  2 21:04:02 CEST 2023"
}

PLAY RECAP *********************************************************************
```
