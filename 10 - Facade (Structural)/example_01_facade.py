"""
============================================================
Example: Video Conversion Facade
Pattern: Facade (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You are building a video streaming app. You use a complex 3rd party
video conversion library (simulated here) with many classes: 
VideoFile, CodecFactory, BitrateReader, AudioMixer, etc.

To convert a video, you have to orchestrate 6 different classes in 
a specific order. If you put this logic in your UI code, your UI 
becomes tightly coupled to the video library.

Instead, you build a `VideoConverterFacade` that exposes a single
method: `convert(filename, format)`.

KEY INSIGHT:
------------
The client only talks to the Facade. The Facade orchestrates the
subsystem. If the 3rd party library changes its API, you only have
to update the Facade, not your entire application.

============================================================
"""

# ─── COMPLEX SUBSYSTEM (Simulated 3rd Party Library) ───

class VideoFile:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        print(f"  [Subsystem] Loaded video file: {filename}")

class OggCompressionCodec:
    def get_type(self) -> str:
        return "ogg"

class MPEG4CompressionCodec:
    def get_type(self) -> str:
        return "mp4"

class CodecFactory:
    @staticmethod
    def extract(file: VideoFile) -> str:
        print(f"  [Subsystem] Extracting codec from {file.filename}...")
        return "mp4" if file.filename.endswith(".mp4") else "ogg"

class BitrateReader:
    @staticmethod
    def read(filename: str, source_codec: str) -> str:
        print(f"  [Subsystem] Reading file {filename} with codec {source_codec}...")
        return f"buffer_of_{filename}"

    @staticmethod
    def convert(buffer: str, destination_codec: object) -> str:
        print(f"  [Subsystem] Converting {buffer} to target codec...")
        return f"converted_{buffer}"

class AudioMixer:
    @staticmethod
    def fix_audio(result: str) -> str:
        print("  [Subsystem] Fixing audio sync issues...")
        return f"audio_synced_{result}"


# ─── FACADE ────────────────────────────────────────────

class VideoConverterFacade:
    """
    The Facade. It hides the complexity of the subsystem from the client.
    It provides a simple interface for the most common use case.
    """
    
    def convert(self, filename: str, format: str) -> str:
        print(f"\n🎬 Facade starting conversion of '{filename}' to '{format}'...")
        
        # The Facade handles all the ugly orchestration!
        file = VideoFile(filename)
        source_codec = CodecFactory.extract(file)
        
        if format == "mp4":
            destination_codec = MPEG4CompressionCodec()
        else:
            destination_codec = OggCompressionCodec()
            
        buffer = BitrateReader.read(filename, source_codec)
        result = BitrateReader.convert(buffer, destination_codec)
        final_result = AudioMixer.fix_audio(result)
        
        print("🎬 Facade finished conversion!")
        return final_result


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FACADE PATTERN - Video Conversion")
    print("=" * 60)
    
    # Client Code
    # Look how simple the client code is! 
    # It knows nothing about CodecFactory, AudioMixer, or BitrateReader.
    
    converter = VideoConverterFacade()
    
    # Convert an OGG to MP4
    mp4_file = converter.convert("vacation_video.ogg", "mp4")
    print(f"\nClient received: {mp4_file}")
    
    print("\n✅ Facade pattern demonstrated successfully!")
