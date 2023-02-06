# Chrome Extensions for offline web browsers

This repo is created to download the latest Google chrome extensions for offline installation.

### Use case:
Imagine a scenario where you need to install your chrome extension on a web browser that doesn't have any internet connection.

### Requirements: 
This script use python3

### Credits: 
https://gist.github.com/luizoti/20e41bb0ea30f2ce0170b657e1238499



### Usage:


1.Run the python file to download the extensions
```
python3 ChromeAppDownloader.py
```

2.Run the following PS command in **command prompt** and generate the **_Checksum_SHA256.txt_**

_Command for table format:_
```
powershell -command "Get-Date | Tee-Object -Append -FilePath Checksum_SHA256.txt; Get-FileHash Extensions\* | Select-Object -Property Algorithm, Hash, @{n='Path'; e={$_.Path.Substring(($PWD).Path.Length + 1)}} | Format-Table | Tee-Object -Append -FilePath Checksum_SHA256.txt"
```
**or**

_Command for list format:_

```
powershell -command "Get-Date | Tee-Object -Append -FilePath Checksum_SHA256.txt; Get-FileHash Extensions\* | Select-Object -Property Algorithm, Hash, @{n='Path'; e={$_.Path.Substring(($PWD).Path.Length + 1)}} | Format-List -Property Path, Hash, Algorithm | Tee-Object -Append -FilePath Checksum_SHA256.txt"

```
3.Move the **_Checksum_SHA256.txt_** to **_Extensions/_** folder
```
move /Y Checksum_SHA256.txt Extensions\
```

### Screenshots:

**Screenshot-1:** Before executing the commands
<kbd>![Steps](images/Screenshot-1.png)</kbd>

**Screenshot-2:** Above 3 commands executed in windows command prompt
<kbd>![Steps](images/Screenshot-2.png)</kbd>

**Screenshot-3:** After executing the commands
<kbd>![Steps](images/Screenshot-3.png)</kbd>

**Screenshot-4** List of downloaded extensions
<kbd>![Steps](images/Screenshot-4.png)</kbd>

**Screenshot-5** Output of _Checksum_SHA256.txt_ file
<kbd>![Steps](images/Screenshot-5.png)</kbd>

