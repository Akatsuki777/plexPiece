# plexPiece

## Description
This is a small Python script that renames and moves already-downloaded episodes of *One Pace* into an appropriate folder/file structure so they can be indexed by Plex. It then adds metadata to seasons and episodes via `plexapi`.

---

## Usage

1. Clone the repository into the root of your One Pace folder:
   ```bash
   cd /path/to/one/pace/ && git clone https://github.com/Akatsuki777/plexPiece.git
   ```

2. Change into the repository directory and run the setup script:
   ```bash
   cd plexPiece
   python3 setup.py
   ```
   Enter the Plex Host and Plex Token when prompted.

3. Run the metadata script:
   ```bash
   python3 makeMetaData.py
   ```

---

## Important Files
The following files in the folder are critical for the operation of this script:

- `One Pace Episode Guide - Meta.csv`: Contains the Episode details from official One Pace release.
- `One Pace Episode Guide - Season Sheet.csv`: Contains the Season details from official One Pace release.
- `onePieceMetaData.json`: This is the collection of all episodes, their title, summary and release dates.
- `onePieceSeasonData.json`: This contains the season titles and summaries

---

## Season Cover Images
You may populate the `One_Piece_Cover_Images` folder with cover images to use for seasons.  
Name images using the following format:

```
Season XX - Description.extension
```

Where `XX` is the season number (prepend a zero if the season number is a single digit).

---

## Additional Notes / Helper Scripts

There are some helper scripts in Python and JavaScript:

- **`appScript.js`**  
  This script can be added to a copy of the One Pace Database Google Sheet to extract episode and season info when the data in this script is outdated.

- **`buildSeasonData.js`**  
  Used in the browser JS console to extract all arc/season information (note: the Gaimon Arc is absent and must be added manually).  
  **Do not use this script if you do not understand what it does.** Running arbitrary code in the browser console can be dangerous and may expose or delete sensitive data.

- **`scrapeWikiData.js`**  
  Scrapes episode data from Wikipedia. This runs in the browser JS console and **must not be run** unless you understand what it does.

- **`getEpisodeThumbnails.py`**  
  For an additional feature that is not yet implemented. It pulls available episode thumbnails from the Kitsu API. The data are incomplete (only 53 thumbnails available).

---

## Data Sources
All data used by this script were obtained from publicly available sources.
Content from Wikipedia, licensed under CC BY-SA 4.0.

---

## Disclaimer
I do not condone or encourage piracy of any media.  
This software is provided as a proof of concept to demonstrate the process of adding metadata via `plexapi`.
