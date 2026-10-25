FROM python:3.13

# Add environment variables
ADD .env .

# Import required packages
ADD ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add helper data file
ADD ./HelperData/ ./HelperData/

# Add the main objects
ADD ./Objects/ ./Objects/

# Add all the cogs
ADD ./cogs/ ./cogs/

# Add the main bot
ADD bot.py .

# Define ports
ENV PORT=8080
EXPOSE 8080

# Run our Python script
CMD ["python", "bot.py"]