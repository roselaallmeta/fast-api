import asyncio
import asyncpg

createStatements = {
    "investment_type": """
			CREATE TYPE investment_type AS ENUM('equity', 'loan', 'grant');
    """,

    "industries": """
			CREATE TYPE industries AS ENUM(
		'technology',
    'finance',
    'healthcare',
    'education',
    'energy',
    'real_estate',
    'transportation',
    'retail',
    'other',
		'media');
    """,

    "funding_stage": """
			CREATE TYPE investment_type AS ENUM('pre_seed',
    'seed',
    'series_a',
    'series_b',
    'series_c',
    'series_d_plus',
    'venture_round',
    'private_equity',
    'debt_financing',
    'grant',
    'ipo',
    'acquired');
    """,


    "currency": """
			CREATE TYPE currency AS ENUM('USD',
        'EUR',
        'JPY',
        'ALL',
        'GBP',
        'CHF',
        'CAD',
        'AUD',
        'CNY',
        'SEK',
        'NZD',
        'KRW',
        'SGD',
        'NOK',
        'INR');
    """,

                "gender": """
			CREATE TYPE gender AS ENUM('male', 'female', 'other');
    """,


                "user_roles": """
			CREATE TYPE user_role AS ENUM('founder', 'investor', 'guest', 'institution', 'admin', 'business');
    """,


    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
						user_role user_role NOT NULL,
            email VARCHAR(255) UNIQUE,
						gender gender NOT NULL
        );
    """,


    "user_profiles": """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            profile_id INT NOT NULL REFERENCES users(id),
            phone_number VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP DEFUALT NOW(),
            is_active BOOLEAN
        );
    """,

                "pitch_decks": """
        CREATE TABLE IF NOT EXISTS pitch_decks (
            id SERIAL PRIMARY KEY,
						pitch_id INT NOT NULL REFERENCES ventures(id) ON DELETE CASCADE,
						title VARCHAR(250) NOT NULL,
						file_url TEXT NOT NULL,
						description TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """,

    "ventures": """
        CREATE TABLE IF NOT EXISTS ventures (
            id SERIAL PRIMARY KEY,
						venture_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
						venture_id INT NOT NULL REFERENCES pitch_decks(id) ON DELETE CASCADE,
            name VARCHAR(255),
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(255),
					  # founderId
            description VARCHAR(1000),
						industry industry NOT NULL,
            created_at TIMESTAMP,
            funding_stage funding_stage NOT NULL,
            website_url VARCHAR(255),
            funding_goal DECIMAL(18,2),
						total_funding DECIMAL(18,2),
						valuation NUMERIC(18,2)
						# pitch deck si foreign key
            is_active BOOLEAN
        );
    """,

    "investments": """
        CREATE TABLE IF NOT EXISTS investments (
            id SERIAL PRIMARY KEY,
						venture_id INT NOT NULL REFERENCES ventures(id) ON DELETE CASCADE,
						user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,				
            title VARCHAR(255),
            amount NUMERIC(18,2),
						investment_type investment_type NOT NULL,
            equity_percent NUMERIC(5,2),
            currency currency NOT NULL,
            invested_on TIMESTAMP,
            description VARCHAR(1000)
        );
    """,


    "teams": """
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            number_of_members INT NOT NULL,
            names VARCHAR(255),
            roles VARCHAR(1000),
            startup_before BOOLEAN
        );
    """,


                "bank_accounts": """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            id SERIAL PRIMARY KEY,
						account_number TEXT UNIQUE NOT NULL,
						IBAN TEXT UNIQUE,
						BIC TEXT UNIQUE,
						CURRENCY CURRENCY NOT NULL,
						BALANCE NUMERIC(18,2)
        );
    """
}


async def main():
    conn = await asyncpg.connect('postgresql://admin@localhost:5433/main')

    for statement in createStatements.values():
        await conn.execute(statement)

    await conn.close()  # duhet te jete jasht loop , ne menyre qe per cdo tabele te re qe krijon te mos hapet databaza prap


asyncio.run(main())

