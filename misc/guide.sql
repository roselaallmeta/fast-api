--     VENTURE_MEMBERS
-- MEMBER_ID | VENTURE_ID
-- rosela    |     2
-- enes      |     2
-- rosela    |     3
-- albi      |     2
-- bora      |     2


-- ---

-- <!-- GET ALL MEMBERS OF VENTURE 2 -->

-- SELECT vm.member_id FROM main.venture_members vm WHERE vm.venture_id = 2

-- [rosela, enes, bora]

-- <!-- ADD JOIN -->

-- SELECT u.user_id,
--   u.name,
--   u.gender,
--   u.role,
-- 	vm.member_id
-- FROM main.venture_members vm 
-- JOIN main.users u
-- 	ON u.user_id = vm.member_id
-- WHERE vm.venture_id = 2

-- <!-- RES -->

--              USERS (U)            |  VENTURE_MEMBERS (VM)
-- ----------------------------------------------------------
-- enes | Enes Bala | male | founder |       enes
-- rosela | Rosela Allmeta | female  |      rosela


-- <!-- GET ALL VENTURES WHERE ROSELA IS A MEMBER -->

-- SELECT v.id, v.name, v.valuation, vm.member_id,
-- FROM main.venture_members vm
-- JOIN main.ventures v
-- 	ON v.id = vm.venture_id
-- WHERE vm.member_id = 'rosela'

-- -- RES

--           VENTURES (V)            |  VENTURE_MEMBERS (VM)
-- -----------------------------------------------------------
-- id         name        valuation  |        member_id
-- -----------------------------------------------------------
-- 2    |    merre    |     400,000  |        rosela
-- 3    |     jepi    |    1,600,000 |        rosela

