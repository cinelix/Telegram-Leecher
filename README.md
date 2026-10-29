![](https://user-images.githubusercontent.com/125879861/255391401-371f3a64-732d-4954-ac0f-4f093a6605e1.png)

<br>


<p align="center">
  <strong>High-performance, Colab-powered transloading bot built on Pyrogram.</strong><br>
  Transfer files and folders from direct links, Mega, YouTube/video platforms, Google Drive, and Telegram straight to your Telegram chats or Google Drive storage.
</p>

<p align="center">
  <a href="https://colab.research.google.com/drive/12hdEqaidRZ8krqj7rpnyDzg1dkKmvdvp?usp=sharing"><img src="https://user-images.githubusercontent.com/125879861/255389999-a0d261cf-893a-46a7-9a3d-2bb52811b997.png" alt="Open In Colab" width="160"></a>
  <a href="https://t.me/Colab_Leecher"><img src="https://img.shields.io/badge/Telegram-Channel-blue?logo=telegram" alt="Telegram Channel"></a>
  <a href="https://t.me/Colab_Leecher_Discuss"><img src="https://img.shields.io/badge/Telegram-Discussion-blue?logo=telegram" alt="Telegram Group"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-green.svg" alt="License"></a>
</p>

---

## 📑 Table of Contents
1. [Key Features](#-key-features)
2. [Supported Sources](#-supported-sources)
3. [Prerequisites & Getting Credentials](#-prerequisites--getting-credentials)
4. [Deployment Instructions](#-deployment-instructions)
5. [Bot Command Reference](#-bot-command-reference)
6. [Input Link Syntax & Advanced Options](#-input-link-syntax--advanced-options)
7. [Operational Warnings & Limits](#-operational-warnings--limits)
8. [License](#-license)

---

## ⚡ Key Features

- **Blazing Transfer Rates:** Up to 200 MiB/s download and 30+ MiB/s upload using Google Colab compute.
- **Dual Destination Modes:**
  - `Leech`: Uploads files directly to your private channel or direct messages.
  - `Mirror`: Direct sync to your mounted Google Drive instance.
- **Smart Archive Handling:**
  - Automatically unzips/extracts `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, and multi-part archives (`.001`, `.part1.rar`, `.z01`).
  - Supports password-protected archiving and extraction.
  - Automatic 2 GB split handling (or zipping) for files exceeding Telegram's upload limits.
- **Hardware-Accelerated Video Conversion:**
  - Converts unsupported media to clean `.mp4` or `.mkv` using FFmpeg (with NVENC GPU support if available).
  - Automatically captures thumbnails and video duration metadata for seamless streaming.
- **In-Chat Settings Panel:**
  - Configure caption formats (Monospace, Bold, Italic, Underline), custom prefixes, custom suffixes, and persistent thumbnails via Telegram inline buttons.

---

## 🔗 Supported Sources

| Source | Status | Engine / Notes |
| :--- | :---: | :--- |
| **Direct HTTP / HTTPS Links** | ✅ Supported | Aria2c Multi-connection Engine |
| **YouTube & 2,000+ Video Portals** | ✅ Supported | `yt-dlp` integrated pipeline |
| **Telegram Messages / Channels** | ✅ Supported | Native MTProto stream extraction |
| **Google Drive Files & Folders** | ✅ Supported | Google Drive REST API v3 |
| **Mega.nz Links** | ✅ Supported | `megatools` async worker |
| **Local Colab Paths** | ✅ Supported | Direct filesystem transloading (`/drupload`) |
| **Torrents / Magnet Links** | ❌ Blocked | Prohibited under Google Colab Terms |

---

## 🔑 Prerequisites & Getting Credentials

Before executing the notebook, gather the following credentials:

1. **`API_ID` & `API_HASH`**:
   - Go to [my.telegram.org](https://my.telegram.org) and log in.
   - Click on **API Development Tools**.
   - Create a new application and save your `api_id` (numeric) and `api_hash` (alphanumeric string).

2. **`BOT_TOKEN`**:
   - Open Telegram and message [@BotFather](https://t.me/BotFather).
   - Send `/newbot`, assign a name and username, and copy the HTTP API token provided.

3. **`USER_ID`**:
   - Message [@userinfobot](https://t.me/userinfobot) or [@MissRose_bot](https://t.me/MissRose_bot) on Telegram to get your numeric account ID.

4. **`DUMP_ID` (Channel ID)**:
   - Create a **Private Telegram Channel**.
   - Add your bot to this channel as an **Administrator** with full posting permissions.
   - Forward a message from this channel to [@userinfobot](https://t.me/userinfobot) or [@JsonDumpBot](https://t.me/JsonDumpBot) to obtain the channel ID.
   - *Format:* Channel IDs must start with `-100` (e.g., `-1002145678901`).

---

## 🚀 Deployment Instructions

### Method 1: Google Colab (Recommended)

1. Open the [Official Colab Notebook](https://colab.research.google.com/drive/12hdEqaidRZ8krqj7rpnyDzg1dkKmvdvp?usp=sharing).
2. If mirroring to Google Drive, execute the **Mount Google Drive** cell and complete authorization.
3. In the **Main Code** cell, insert your credentials:
   ```python
   API_ID = 12345678
   API_HASH = "your_api_hash_here"
   BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ"
   USER_ID = 987654321
   DUMP_ID = -1002145678901
   ```
4. Click **Run Cell** (`Ctrl + Enter`).
5. Open your bot in Telegram and send `/start`.


---

## 🤖 Bot Command Reference

Send these commands directly to the bot in private messages:

| Command | Description |
| :--- | :--- |
| `/start` | Verify if the bot instance is active and responsive. |
| `/instruction` | Show this interactive command guide inside Telegram. |
| `/tupload` | Request download links to upload directly to **Telegram** (Leech). |
| `/gdupload` | Request download links to upload directly to **Google Drive** (Mirror). |
| `/drupload` | Upload an existing folder path from the Colab local disk. |
| `/ytupload` | Download and convert links through `yt-dlp` (YouTube, Vimeo, etc.). |
| `/settings` | Open the interactive configuration panel. |
| `/setname <name>` | Assign a custom filename for the upcoming download task. |
| `/zipaswd <pass>` | Set an encryption password for output `.zip` archives. |
| `/unzipaswd <pass>` | Provide the extraction password for locked archives. |
| `/help` | Display quick tips and support community channels. |

---

## 📝 Input Link Syntax & Advanced Options

When the bot prompts you for download links after running `/tupload` or `/gdupload`, you can pass multiple URLs alongside optional metadata tags.

### Standard Batch Download
Provide one link per line:
```text
https://example.com/file1.mp4
https://example.com/file2.zip
```

### Custom Filename, Zip Password & Unzip Password
You can append custom arguments at the end of your message using specific bracket enclosures:
- `[Custom_File_Name.ext]` ➔ Overrides the file's saved name.
- `{Zip_Password}` ➔ Sets a password on the final output `.zip` archive.
- `(Unzip_Password)` ➔ Tells the extractor which password to use for locked source archives.

#### Example:
```text
https://example.com/archive.rar
[Project_Assets_2025.zip]
{MyNewZipPass123}
(SourceArchivePass)
```

### Supported Processing Modes
After sending links, choose an action from the inline buttons:
- **Regular**: Downloads and uploads the files without changing container structures.
- **Compress**: Compresses all downloaded files into a `.zip` archive before uploading.
- **Extract**: Unpacks `.zip`, `.rar`, or `.7z` archives and uploads their individual contents.
- **UnDoubleZip**: Extracts an archive, flattens the hierarchy, and re-compresses it into an organized `.zip`.

---

## ⚙️ Interactive Settings Reference

Use `/settings` to adjust your preferences:
- **Upload Type**: Toggle between `Media` (streams natively in Telegram players) and `Document` (preserves uncompressed binary payload).
- **Video Convert**: Enable or disable automatic transcode of non-standard formats into web-friendly `.mp4` or `.mkv`.
- **Quality Preset**: Toggle between `High` (slower, lossless preset) and `Low` (faster, compressed preset).
- **Caption Font**: Switch between `Monospace`, `Bold`, `Italic`, `Underlined`, or `Regular`.
- **Prefix / Suffix**: Automatically attach tags or branding to all uploaded file captions.
- **Thumbnail**: Send any photo to the bot to use it as a custom video/document cover.

---

## ⚠️ Operational Warnings & Limits

1. **Google Colab Disconnections:**
   - Free Colab instances disconnect if the browser tab remains idle or exceeds timeout limits (~12 hours max per session).
   - Use the built-in audio player keep-alive cell to help prevent premature browser throttling.

2. **File Size Limits:**
   - Standard Telegram Bot API upload limit is **2,000 MB (2 GB)** per file.
   - Any single file exceeding 2 GB will be automatically split into segmented archives (`.zip.001`, `.zip.002`) to ensure successful delivery.

3. **Colab Disk Quota:**
   - Standard Colab runtimes offer ~80–100 GB of free storage.
   - Always clear old files or process batches within disk limits to avoid out-of-space aborts (`Errno 28: No space left on device`).

4. **Colab Terms of Service Notice:**
   - Downloading **Torrents** or running peer-to-peer file-sharing utilities violates Google Colab's acceptable use policy and will result in immediate runtime termination.

---

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
See the [LICENSE](LICENSE) file for complete details.
```
