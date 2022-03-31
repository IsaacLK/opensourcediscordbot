import os
import discord
import random
from discord.ext import commands
import pydrive
#from dotenv import load_dotenv
import google.oauth2.credentials
import google_auth_oauthlib.flow
import ffmpeg
import youtube_dl
token = os.getenv("TOKEN")
client = commands.Bot(command_prefix='.')
client.remove_command('help')
@client.event
async def on_ready():
    print(f'{client.user} now online')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for .help | https://github.com/IsaacLK/opensourcediscordbot'))
    #print("="*40, "CPU Info", "="*40)
    # number of cores
    #print("Physical cores:", psutil.cpu_count(logical=False))
    #print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    #cpufreq = psutil.cpu_freq()
    #print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    #print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    #print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    #print("CPU Usage Per Core:")
    #for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    #    print(f"Core {i}: {percentage}%")
    #print(f"Total CPU Usage: {psutil.cpu_percent()}%")
@client.command()
async def help(ctx):
  embed=discord.Embed(title="Commands:", color=0x003b46)
  embed.add_field(name=".help", value="Displays this list", inline=True)
  embed.add_field(name=".hello", value="Hello!", inline=True)
  embed.add_field(name=".github", value="Link to my Github where this bot is hosted!", inline=True)
  embed.add_field(name=".ping", value="Displays bot ping", inline=True)
  embed.add_field(name=".pfp", value="Displays your PFP as image", inline=True)
  embed.add_field(name=".ytdownload", value="Downloads a youtube video (usage example: .ytdownload https://youtube.com/video/asdji23Jdjio or something like that.) Add mp3 to end of command to output as audio (example ytdownload https://youtube.com/video/asdji23Jdjio mp3)", inline=True)
  await ctx.send(embed=embed)
@client.command()
async def hello(ctx):    
    embed=discord.Embed(title="Hello!", color=0x003b46)
    await ctx.send(embed=embed)
@client.command()
async def github(ctx):
    embed=discord.Embed(title="Click here to open up the GitHub!", url="https://github.com/IsaacLK/opensourcediscordbot", color=0x003b46)
    await ctx.send(embed=embed)
@client.command()
async def ping(ctx):
    ping = client.latency
    embed=discord.Embed(title="The bot's ping is "+ str(round(ping * 1000)) + "ms", color=0x003b46)
    await ctx.send(embed=embed)
@client.command()
async def pfp(ctx):
  await ctx.send(ctx.author.avatar_url)
@client.command()
async def ytdownload(ctx, link, audio = ""):
  
  print("downloading")
  try:
    os.remove("download.mp4")
  except:
    pass
  try:
    os.remove("download.mp4.mkv")
  except:
    pass
  try:
    os.remove("resized.mp4")
  except:
    pass
  try:
    os.remove("finished.mov")
  except:
    pass
  try:
    os.remove("audio.mp3")
  except:
    pass
  embed=discord.Embed(title="Downloading & Compressing the video/audio! The wait is about 2-4 minutes because we got slow servers. ", color=0x003b46)
  await ctx.send(embed=embed)
  
  video = link
  ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

  with ydl:
      result = ydl.extract_info(
          video,
          download=False # We just want to extract the info
      )
  vidlength = result['duration']
  print("video length is ",vidlength)

  #yt = pytube.YouTube(video)
  #print(yt)
  #title = yt.title

  #print(f"Ok, about to download: {title}!")
  
  #print('length is', yt.length)
  lengthM = vidlength / 60
  if audio == "mp3" and lengthM >= 5:
    
    embed=discord.Embed(title="Cannot Download Video (Error: Audio Over 5 minutes not supported)", color=0x003b46)
    await ctx.send(embed=embed)
  else:
    if lengthM >= 10:
      embed=discord.Embed(title="Cannot Download Video (Error: Videos greater than 10 minutes are not supported)", color=0x003b46)
      await ctx.send(embed=embed)
    else:
      if audio == "mp3":
        
        ydl_opts = {'outtmpl': 'audio.mp3', 'format': 'bestaudio/best', 'extractaudio' : True, 'audioformat' : "mp3",'noplaylist' : True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          ydl.download([video])
        file_size = os.path.getsize('audio.mp3')
        if file_size <= 7777777:
          
          await ctx.send(file=discord.File(r'audio.mp3'))
        else:
          print("File size requirement not met")
      else:
      
        
        ydl_opts = {'outtmpl': 'download.mp4', 'format': 'worst'}
        # 'format': 'worst'
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          ydl.download([video])   
        try:
          os.rename('download.mp4.mkv', 'download.mp4')
        except:
          pass
        try:
          os.rename('download.mkv', 'download.mp4')
        except:
          pass
          file_size = os.path.getsize('download.mp4')
          print("File Size is :", file_size, "bytes")
          if file_size <= 7777777:
            await ctx.send(file=discord.File(r'download.mp4'))
          else:
            
            if file_size <= 7777777:
              await ctx.send(file=discord.File(r'download.mp4'))
            else:
              video_full_path = "download.mp4"
              output_file_name = "finished.mov"
              target_size = 8 * 1024
              #clip = mp.VideoFileClip(video_full_path)
              #clip_resized = clip.resize(height=360) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
              min_audio_bitrate = 48000
              max_audio_bitrate = 96000
              #video_full_path = "resized.mp4"
              probe = ffmpeg.probe(video_full_path)
              # Video duration, in s.
              duration = float(probe['format']['duration'])
              # Audio bitrate, in bps.
              audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
              # Target total bitrate, in bps.
              target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

              
              if 10 * audio_bitrate > target_total_bitrate:
                  audio_bitrate = target_total_bitrate / 10
                  if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                      audio_bitrate = min_audio_bitrate
                  elif audio_bitrate > max_audio_bitrate:
                      audio_bitrate = max_audio_bitrate
              
              video_bitrate = target_total_bitrate - audio_bitrate
              
              i = ffmpeg.input(video_full_path)
              ffmpeg.output(i, os.devnull,
                            **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mov'}
                            ).overwrite_output().run()
              ffmpeg.output(i, output_file_name,
                            **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                            ).overwrite_output().run()
              await ctx.send(file=discord.File(r'finished.mov'))
client.run(token)
