# NotesAutoSync

Script for automatic synchronization of notes (information) in the Codeberg (GitHub) repository using SSH.

## Startup instructions

### **Linux** 
#### 1. Clone the repository to your device
```bash
    git clone https://codeberg.org/femto/NotesAutoSync.git
```
or
```bash
    git clone https://github.com/AnDsergey13/NotesAutoSync.git
```
#### 2. Go to the folder with the script
```bash
    cd NotesAutoSync
```
#### 3. Copy AutoSync.py and AutoSync.sh to the root of the synchronized repository
```bash
    cp AutoSync.py /home/USER/Notes/AutoSync.py
    cp AutoSync.sh /home/USER/Notes/AutoSync.sh
    # Instead of /home/USER/Work/Notes/* enter your path where the notes are located
    # where USER is your username
```
#### 4. Go to notes folder
```bash
    cd /home/USER/Notes
```
#### 5. If necessary, configure the note synchronization delay in AutoSync.py
```python
    # Time in seconds
    TIME_UPDATE = 30
```
❗❗❗ Before you run the python script, you need to configure [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) **no password** for a synchronized repository. Otherwise the script will not work.

To test your SSH connection you need to write
```bash
    # for GitHub
    ssh -T git@github.com
```
or
```bash
    # for Сodeberg
    ssh -T git@codeberg.org 
```

#### 6. Normal launch
```bash
    python AutoSync.py
```
Abort the process **Ctrl + C**

#### 7. Start in automatic mode
Add the following line to application startup
```bash
    bash /home/USER/Notes/AutoSync.sh
    # Instead of /home/USER/Work/Notes/* enter your path where the notes are located
    # where USER is your username
```
All. When the system starts, the script will start working automatically.

---
### **Windows** - TODO
---
### **Android** - TODO