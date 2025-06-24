import sqlite3
import asyncio
import asyncpg

conn = sqlite3.connect(":memory:")  # creates in-memory DB
cursor = conn.cursor()



createTables = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        );
    """,

    "user_profiles": """
        CREATE TABLE IF NOT EXISTS user_profiles (
            profile_id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id),
            gender VARCHAR(10),
            phone_number VARCHAR(20) NOT NULL,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN
        );
    """,

    "startups": """
        CREATE TABLE IF NOT EXISTS startups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(255),
            description VARCHAR(1000),
            created_at TIMESTAMP,
            funding_stage VARCHAR(50),
            website_url VARCHAR(255),
            total_funding FLOAT,
            is_active BOOLEAN
        );
    """,

    "roles": """
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            user_role VARCHAR(50)
        );
    """,

    "investments": """
        CREATE TABLE IF NOT EXISTS investments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            amount FLOAT,
            equity_percent FLOAT,
            currency VARCHAR(10),
            invested_on TIMESTAMP,
            notes VARCHAR(1000)
        );
    """,

    "industries": """
        CREATE TABLE IF NOT EXISTS industries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        );
    """,

    "team": """
        CREATE TABLE IF NOT EXISTS team (
            id SERIAL PRIMARY KEY,
            number_of_members INT NOT NULL,
            names VARCHAR(255),
            roles VARCHAR(1000),
            startup_before BOOLEAN
        );
    """


		
}


async def main():
	conn = await asyncpg.connect('postgresql://postgres@localhost/main')


	for statement in createTables.values():
		await conn.execute(statement)
		

	await conn.close() # duhet te jete jasht loop , ne menyre qe per cdo tabele te re qe krijon te mos hapet databaza prap

	
asyncio.run(main())








            

    

#creating the tables in the in memory database


			










# baseIndustries = [
#     'FinTech',
#     'HealthTech',
#     'EdTech',
#     'SaaS',
#     'eCommerce',
#     'ClimateTech',
#     'AI & Machine Learning',
#     'Cybersecurity',
#     'Biotech',
#     'Other'
# ]








# for index, item in enumerate(baseIndustries):
#     text = f"('{item}')"
    
#     if index == len(baseIndustries) - 1:
#         text += ';'
#     else:
#         text += ',\n'
    
#     baseIndustriesQuery += text

# print(baseIndustriesQuery)

# # db.run(baseIndustriesQuery)



