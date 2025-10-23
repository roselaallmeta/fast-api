import asyncpg
import asyncio


dropStatements = [
    "DROP TYPE IF EXISTS main.investment_type CASCADE;",
    "DROP TYPE IF EXISTS main.status CASCADE;",
    "DROP TYPE IF EXISTS main.user_status CASCADE;",
    "DROP TYPE IF EXISTS main.venture_status CASCADE;",
    "DROP TYPE IF EXISTS main.industries CASCADE;",
    "DROP TYPE IF EXISTS main.gender CASCADE;",
    "DROP TYPE IF EXISTS main.user_role CASCADE;",
    "DROP TABLE IF EXISTS main.users CASCADE;",
    "DROP TABLE IF EXISTS main.user_profiles CASCADE;",
    "DROP TABLE IF EXISTS main.ventures CASCADE;",
    "DROP TABLE IF EXISTS main.venture_teams CASCADE;",
    "DROP TABLE IF EXISTS main.investments CASCADE;",
    "DROP TABLE IF EXISTS main.team_members CASCADE;",
    "DROP TABLE IF EXISTS main.teams CASCADE;",
    "DROP TYPE IF EXISTS main.funding_stage CASCADE;",
    "DROP TYPE IF EXISTS main.currency CASCADE;",
    "DROP TYPE IF EXISTS main.gender CASCADE;",
    "DROP TYPE IF EXISTS main.user_role CASCADE;",
    "DROP TABLE IF EXISTS main.venture_members CASCADE;",
    "DROP TABLE IF EXISTS main.document CASCADE;",
    "DROP TABLE IF EXISTS main.banking_details CASCADE;",
    "DROP TABLE IF EXISTS main.pitch_decks CASCADE;"

    # "SELECT * FROM main.users INNER JOIN main.user_profiles ON main.users.user_id = main.user_profiles.user_id;"
]


createStatements = {

    "investment_type": """
        CREATE TYPE main.investment_type AS ENUM ('equity', 'loan', 'grant');
    """,

    "status": """
        CREATE TYPE main.status AS ENUM ('pending', 'approved', 'rejected');
    """,

    "user_status": """
        CREATE TYPE main.user_status AS ENUM ('active', 'inactive', 'deactivated');
    """,

    "venture_status": """
        CREATE TYPE main.venture_status AS ENUM ('active', 'archived', 'banned');
    """,

    "industries": """
        CREATE TYPE main.industries AS ENUM (
            'technology',
            'finance',
            'healthcare',
            'education',
            'energy',
            'real_estate',
            'transportation',
            'retail',
            'other',
            'media'
        );
    """,

    "funding_stage": """
        CREATE TYPE main.funding_stage AS ENUM(
            'pre_seed', 'seed', 'series_a', 'series_b', 'series_c', 'series_d_plus',
            'venture_round', 'private_equity', 'debt_financing', 'grant', 'ipo', 'acquired'
        );
    """,

    "currency": """
        CREATE TYPE main.currency AS ENUM(
            'USD', 'EUR', 'JPY', 'ALL', 'GBP', 'CHF', 'CAD', 'AUD',
            'CNY', 'SEK', 'NZD', 'KRW', 'SGD', 'NOK', 'INR'
        );
    """,

    "gender": """
        CREATE TYPE main.gender AS ENUM('male', 'female', 'other');
    """,

    "user_role": """
        CREATE TYPE main.user_role AS ENUM('founder', 'investor', 'guest', 'institution', 'admin', 'business');
    """,



    "users": """
        CREATE TABLE IF NOT EXISTS main.users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            role main.user_role NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP DEFAULT NOW()
        );
    """,

    # KA ONE TO ONE RELATIONSHIP ME USERS , NJE USER KA NJE PROFILE, DHE NJE PROFILE BELONGS TO ONE USER
    "user_profiles": """
        CREATE TABLE IF NOT EXISTS main.user_profiles (
        		id SERIAL PRIMARY KEY,
            user_id INT UNIQUE, 
            FOREIGN KEY (user_id) REFERENCES main.users(id),
            gender main.gender NOT NULL, 
            phone_number VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            is_active BOOLEAN,
            industry main.industries NOT NULL,
            description TEXT,
            status main.user_status NOT NULL
        );
    """,


                # SHTO NJE BUTON QE TE BEJ INVEST

    "ventures": """
        CREATE TABLE IF NOT EXISTS main.ventures (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            created_at TIMESTAMP,
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(255),
            description VARCHAR(1000),
            industries main.industries NOT NULL, 
            funding_stage main.funding_stage NOT NULL,
            website_url VARCHAR(255),
            funding_goal DECIMAL(18,2),
            total_funding DECIMAL(18,2),
            valuation NUMERIC(18,2),
            status main.venture_status NOT NULL
        );
    """,

                "teams": """
        CREATE TABLE IF NOT EXISTS main.teams (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """,

    # which team works on which venture

    # many to many relationship

    "venture_teams": """
        CREATE TABLE IF NOT EXISTS main.venture_teams (
            venture_id INT NOT NULL REFERENCES main.ventures(id) ON DELETE CASCADE,
            team_id INT NOT NULL REFERENCES main.teams(id) ON DELETE CASCADE,
            title VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (venture_id, team_id)  
        );
    """,

    # nje venture has multiple members , a member can be apart of multiple ventures


                "venture_members": """
				CREATE TABLE IF NOT EXISTS main.venture_members (
                member_id INT NOT NULL REFERENCES main.users(id) ON DELETE CASCADE,
                venture_id INT NOT NULL REFERENCES main.ventures(id),
                name VARCHAR(255),
                PRIMARY KEY (member_id, venture_id)
        );
		""",


    "investments": """
        CREATE TABLE IF NOT EXISTS main.investments (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES main.users(id) ON DELETE CASCADE,
            venture_id INT NOT NULL REFERENCES main.ventures(id) ON DELETE CASCADE,
            name VARCHAR(255),
            amount NUMERIC(18,2),
            investment_type main.investment_type NOT NULL,
            equity_percent NUMERIC(5,2),
            currency main.currency NOT NULL,
            invested_on TIMESTAMP DEFAULT NOW(),
            description VARCHAR(1000)
        );
    """,




    "team_members": """
        CREATE TABLE IF NOT EXISTS main.team_members (
            team_id INT NOT NULL REFERENCES main.teams(id) ON DELETE CASCADE,
            member_id INT NOT NULL REFERENCES main.users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (team_id, member_id)
        );
    """






    # "document": """
    #     CREATE TABLE IF NOT EXISTS main.document (
    #         id SERIAL PRIMARY KEY,
    #         user_id INT NOT NULL REFERENCES main.users(id) ON DELETE CASCADE,
    #         title VARCHAR(255),
    #         add_document VARCHAR(255),
    #         issue_date TIMESTAMP DEFAULT NOW(),
    #         expiry_date TIMESTAMP DEFAULT NOW(),
    #         content_type TEXT NOT NULL,
    #         uploaded_by TEXT NOT NULL,
    #         description TEXT,
    #         uploaded_at TIMESTAMP DEFAULT NOW(),
    #         status main.status NOT NULL
    #     );
    # """,


    # "banking_details": """
    #     CREATE TABLE IF NOT EXISTS main.banking_details (
    #         id SERIAL PRIMARY KEY,
    #         user_id INT NOT NULL REFERENCES main.users(id),
    #         account_number TEXT UNIQUE NOT NULL,
    #         IBAN TEXT UNIQUE,
    #         BIC TEXT UNIQUE,
    #         bank_name TEXT NOT NULL,
    #         bank_country TEXT NOT NULL,
    #         currency main.currency NOT NULL,
    #         balance NUMERIC(18,2),
    #         is_bank_verified BOOLEAN
    #     );
    # """
}

type_keys = [
    "investment_type",
    "status",
    "user_status",
    "venture_status",
    "industries",
    "funding_stage",
    "currency",
    "gender",
    "user_role"
]


table_keys = [
    "users",
    "user_profiles",
    "ventures",
    "teams",
    "venture_teams",
    "investments",
    "team_members"
]

# "venture_members",
#     "pitch_decks",
#     "investments",
#     "document",
#     "banking_details"


async def main():
    conn = await asyncpg.connect('postgresql://admin:rosi123@localhost:5433/main')

    await conn.execute("CREATE SCHEMA IF NOT EXISTS main;")

    for stmt in dropStatements:
        await conn.execute(stmt)

    for key in type_keys:
        print(f"Creating ENUM: {key}")
        await conn.execute(createStatements[key])

    print('-------------------------------------')

    for key in table_keys:
        print(f"Creating TABLE: {key}")
        await conn.execute(createStatements[key])

    await conn.close()

asyncio.run(main())
