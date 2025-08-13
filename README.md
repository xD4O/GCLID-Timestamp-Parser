GCLID Timestamp Decoder

This Python script decodes a Google Click Identifier (GCLID) and attempts to extract a plausible embedded timestamp.
It supports timestamps stored as microseconds, milliseconds, or seconds since the Unix epoch, returning both UTC and local time (America/New_York by default).

🔍 What It Does

	Prompts the user for a GCLID string.
	Reports the character length of the GCLID.
	Base64 URL–decodes the GCLID.
	Parses Protobuf-style varints inside the decoded data.
	Identifies the most likely timestamp:
	Prefers microseconds > milliseconds > seconds.
	Picks the largest (most recent) value found for each type.

🔍 Prints:

	Raw timestamp integer
	Units assumed
	UTC date/time
	Local date/time (America/New_York)

📋 Example Output

	Enter GCLID: EAIaIQobChMIifjEtcr2jgMVmwpoCB2S2jHOEAEYASAAEgKLWfD_BwE

	Character length: 55
	Timestamp (raw integer): 1754496937049097
	Assumed units: microseconds
	UTC datetime: 2025-08-06T16:15:37.049097+00:00
	Local (America/New_York): 2025-08-06T12:15:37.049097-04:00
 
🛠 Requirements
	-	Python 3.9+ (for zoneinfo)
 	-	No external libraries required.

🛠 Usage
Clone the repository:

	git clone https://github.com/yourusername/gclid-timestamp-decoder.git
	cd gclid-timestamp-decoder

🚀 Run the script:


	python gclid_timestamp.py
	Paste your GCLID when prompted and press Enter.

⚠️ Disclaimer


This script is for educational and forensic analysis purposes only.
Google has not publicly documented the internal structure of GCLIDs.
The timestamp extraction is heuristic and may not always be accurate.

