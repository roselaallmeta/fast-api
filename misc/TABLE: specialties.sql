TABLE: specialties
---
id - name
1 Kardiolog
2 Infermier
---

TABLE: doctors
---
id - name
1 Enes
2 Rosela
---

TABLE: doctor_specialties
---
specialty_id - doctor_id
1 2
2 2
2 1

-- ---

-- SELECT * FROM doctor_specialties WHERE doctor_id = 2 (Rosela)

-- ---
-- Doctor_specialties
-- ---
-- specialty_id - doctor_id
-- 1 2
-- 2 2

-- ---

SELECT specialties.name, specialities.id, doctor_specialties.doctor_id FROM doctor_specialties
JOIN specialties ON specialties.id = doctor_specialties.speciality_id  
WHERE doctor_specialties.doctor_id = 2 // Rosela

1 2
2 2

-> 

Kardiolog 1
Infermier 2








-- user ->  name, password, email, role, created_a, updated_at, last_login

-- user_profiles-> user_id referencon user, gender, number, created at, updated at, is active, industry, description, status

-- venture-> name, created_at, phone number, email, description, industry, funding stage, website url, funding goal, total funding, valuation, status

-- teams -> name, created_at

-- venture_teams -> venture_id, team_id, title, created_at, pk

-- venture_members -> member_id, venture_id, name