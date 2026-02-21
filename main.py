
from function import AIassistant

bot = AIassistant()
bot.load_csv(r"C:\python\python webinnor\dataset.csv")

# First input (Task Description)
bot.get_the_prompt() 

# This will now correctly pause and ask for the filename
bot.run_code() 

















 
