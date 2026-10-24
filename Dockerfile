FROM python:3.13

# Transfer the .env file
ADD ./.env .

# Import required packages
RUN pip install discord.py python-dotenv

# Add helper data file
ADD ./HelperData/botHelper.py ./HelperData/
ADD ./HelperData/exceptions.py ./HelperData/
ADD ./HelperData/helpCommand.py ./HelperData/

# Add the main objects
ADD ./Objects/bracket.py ./Objects/
ADD ./Objects/player.py ./Objects/
ADD ./Objects/pod.py ./Objects/
ADD ./Objects/session.py ./Objects/

# Add all the cogs
ADD ./cogs/edits_cog.py ./cogs/
ADD ./cogs/session_cog.py ./cogs/
ADD ./cogs/views_cog.py ./cogs/

# Add the main bot
ADD bot.py .

# Run our Python script
CMD ["python", "bot.py"]