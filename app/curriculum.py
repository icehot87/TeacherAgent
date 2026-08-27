from typing import List, Dict, Any, Optional
from app.models import GradeLevel, SkillDomain, LessonPlan, ExerciseItem, SkillProgress

CURRICULUM_SKILLS: List[Dict[str, Any]] = [
    # ------------------ JUNIOR KINDERGARTEN (JK) ------------------
    {
        "id": "jk_trace_straight_lines",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.TRACING,
        "title": "Pre-Writing: Straight Road Lines",
        "description": "Trace vertical, horizontal, and diagonal lines from start star to finish flag.",
        "prerequisites": [],
        "icon": "✏️",
        "order": 1
    },
    {
        "id": "jk_trace_curves_waves",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.TRACING,
        "title": "Fine Motor: Ocean Waves & Loops",
        "description": "Trace gentle rolling waves, zig-zags, and bouncy bunny hops.",
        "prerequisites": ["jk_trace_straight_lines"],
        "icon": "🌊",
        "order": 2
    },
    {
        "id": "jk_letter_a_d",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters A, B, C, D",
        "description": "Trace uppercase and lowercase A, B, C, D and identify their starting sounds.",
        "prerequisites": ["jk_trace_straight_lines"],
        "icon": "🅰️",
        "order": 3
    },
    {
        "id": "jk_letter_e_h",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters E, F, G, H",
        "description": "Trace uppercase and lowercase E, F, G, H with stroke guide arrows.",
        "prerequisites": ["jk_letter_a_d"],
        "icon": "🐘",
        "order": 4
    },
    {
        "id": "jk_letter_i_l",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters I, J, K, L",
        "description": "Trace uppercase and lowercase I, J, K, L and circle starting sound pictures.",
        "prerequisites": ["jk_letter_e_h"],
        "icon": "🦁",
        "order": 5
    },
    {
        "id": "jk_letter_m_p",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters M, N, O, P",
        "description": "Trace uppercase and lowercase M, N, O, P and practice sound association.",
        "prerequisites": ["jk_letter_i_l"],
        "icon": "🐵",
        "order": 6
    },
    {
        "id": "jk_letter_q_u",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters Q, R, S, T, U",
        "description": "Trace uppercase and lowercase Q, R, S, T, U with handwriting lines.",
        "prerequisites": ["jk_letter_m_p"],
        "icon": "🚀",
        "order": 7
    },
    {
        "id": "jk_letter_v_z",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.PHONICS,
        "title": "Alphabet Safari: Letters V, W, X, Y, Z",
        "description": "Trace uppercase and lowercase V, W, X, Y, Z and celebrate the full alphabet!",
        "prerequisites": ["jk_letter_q_u"],
        "icon": "🦓",
        "order": 8
    },
    {
        "id": "jk_numbers_1_5",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.NUMERACY,
        "title": "Number Garden: Counting & Tracing 1 to 5",
        "description": "Trace numbers 1, 2, 3, 4, 5 and count cute animals to match the number.",
        "prerequisites": ["jk_trace_straight_lines"],
        "icon": "🔢",
        "order": 9
    },
    {
        "id": "jk_numbers_6_10",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.NUMERACY,
        "title": "Number Garden: Counting & Tracing 6 to 10",
        "description": "Trace numbers 6 through 10, fill ten-frames, and circle correct group counts.",
        "prerequisites": ["jk_numbers_1_5"],
        "icon": "🔟",
        "order": 10
    },
    {
        "id": "jk_shapes_basic",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.SHAPES_COLORS,
        "title": "Shape Detective: Circle, Square, Triangle, Star",
        "description": "Trace and identify basic geometric shapes and match real-life objects.",
        "prerequisites": ["jk_trace_curves_waves"],
        "icon": "🔷",
        "order": 11
    },
    {
        "id": "jk_patterns_ab",
        "grade": GradeLevel.JK,
        "domain": SkillDomain.LOGIC_PATTERNS,
        "title": "Pattern Magic: Simple AB Sequences",
        "description": "Complete fun AB visual patterns (e.g. Star, Heart, Star, Heart, ___).",
        "prerequisites": ["jk_shapes_basic"],
        "icon": "🧩",
        "order": 12
    },

    # ------------------ SENIOR KINDERGARTEN (SK) ------------------
    {
        "id": "sk_cvc_short_a",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.PHONICS,
        "title": "Word Builder: Short 'a' CVC Words",
        "description": "Sound out and write 3-letter CVC words: CAT, BAT, HAT, MAP, SUN.",
        "prerequisites": ["jk_letter_v_z"],
        "icon": "🐱",
        "order": 13
    },
    {
        "id": "sk_cvc_short_e_i",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.PHONICS,
        "title": "Word Builder: Short 'e' & 'i' Words",
        "description": "Practice blending sounds for BED, PEN, PIG, SIT, WIN with picture clues.",
        "prerequisites": ["sk_cvc_short_a"],
        "icon": "🐷",
        "order": 14
    },
    {
        "id": "sk_cvc_short_o_u",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.PHONICS,
        "title": "Word Builder: Short 'o' & 'u' Words",
        "description": "Write words like DOG, FOX, BOX, SUN, BUG, CUP.",
        "prerequisites": ["sk_cvc_short_e_i"],
        "icon": "🐶",
        "order": 15
    },
    {
        "id": "sk_sight_words_1",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.PHONICS,
        "title": "Sight Word Explorers: Level 1",
        "description": "Read, trace, and write high-frequency words: I, see, a, the, like, can.",
        "prerequisites": ["sk_cvc_short_a"],
        "icon": "👁️",
        "order": 16
    },
    {
        "id": "sk_numbers_11_20",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.NUMERACY,
        "title": "Ten Frame Pro: Numbers 11 to 20",
        "description": "Trace teen numbers and count double ten-frames (10 + X).",
        "prerequisites": ["jk_numbers_6_10"],
        "icon": "🎯",
        "order": 17
    },
    {
        "id": "sk_addition_to_5",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.NUMERACY,
        "title": "Picture Addition: Sums up to 5",
        "description": "Count objects in two groups and add them together (2 🍎 + 1 🍎 = 3).",
        "prerequisites": ["jk_numbers_6_10"],
        "icon": "➕",
        "order": 18
    },
    {
        "id": "sk_addition_to_10",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.NUMERACY,
        "title": "Number Bonds: Addition up to 10",
        "description": "Find missing parts that make 10 and solve beginner addition equations.",
        "prerequisites": ["sk_addition_to_5"],
        "icon": "🤝",
        "order": 19
    },
    {
        "id": "sk_subtraction_to_5",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.NUMERACY,
        "title": "Take Away Fun: Subtraction within 5",
        "description": "Cross out objects to subtract and find how many are left.",
        "prerequisites": ["sk_addition_to_5"],
        "icon": "➖",
        "order": 20
    },
    {
        "id": "sk_patterns_aabb",
        "grade": GradeLevel.SK,
        "domain": SkillDomain.LOGIC_PATTERNS,
        "title": "Pattern Pro: AABB & ABC Patterns",
        "description": "Identify and continue complex repeating patterns and fill the missing gaps.",
        "prerequisites": ["jk_patterns_ab"],
        "icon": "🎨",
        "order": 21
    },

    # ------------------ GRADE 1 ------------------
    {
        "id": "g1_phonics_blends",
        "grade": GradeLevel.GRADE1,
        "domain": SkillDomain.PHONICS,
        "title": "Phonics Champ: Beginning Blends",
        "description": "Blend consonant clusters: BL (Blue), CL (Clap), FL (Fly), ST (Star).",
        "prerequisites": ["sk_cvc_short_o_u"],
        "icon": "🌟",
        "order": 22
    },
    {
        "id": "g1_sentence_writing",
        "grade": GradeLevel.GRADE1,
        "domain": SkillDomain.READING_WRITING,
        "title": "Sentence Crafter: Simple Sentences",
        "description": "Write complete sentences with a capital letter, finger spaces, and period.",
        "prerequisites": ["sk_sight_words_1"],
        "icon": "✍️",
        "order": 23
    },
    {
        "id": "g1_reading_passage_1",
        "grade": GradeLevel.GRADE1,
        "domain": SkillDomain.READING_WRITING,
        "title": "Story Time: The Friendly Puppy",
        "description": "Read a short 4-sentence decodable passage and answer 3 multiple choice questions.",
        "prerequisites": ["g1_sentence_writing"],
        "icon": "📖",
        "order": 24
    },
    {
        "id": "g1_math_addition_20",
        "grade": GradeLevel.GRADE1,
        "domain": SkillDomain.NUMERACY,
        "title": "Math Mastery: Addition within 20",
        "description": "Use doubles (5+5, 6+6) and count-on strategies to add up to 20.",
        "prerequisites": ["sk_addition_to_10"],
        "icon": "🚀",
        "order": 25
    },
    {
        "id": "g1_math_place_value",
        "grade": GradeLevel.GRADE1,
        "domain": SkillDomain.NUMERACY,
        "title": "Place Value Explorer: Tens & Ones",
        "description": "Group base-10 rods and unit cubes to represent two-digit numbers.",
        "prerequisites": ["sk_numbers_11_20"],
        "icon": "🧱",
        "order": 26
    },

    # ------------------ GRADE 2 ------------------
    {
        "id": "g2_digraphs_vowels",
        "grade": GradeLevel.GRADE2,
        "domain": SkillDomain.PHONICS,
        "title": "Spelling Master: Digraphs & Vowel Teams",
        "description": "Master CH, SH, TH, WH and long vowel teams (EA, OA, AI, AY).",
        "prerequisites": ["g1_phonics_blends"],
        "icon": "🏆",
        "order": 27
    },
    {
        "id": "g2_reading_passage_2",
        "grade": GradeLevel.GRADE2,
        "domain": SkillDomain.READING_WRITING,
        "title": "Adventure Reading: The Secret Treehouse",
        "description": "Read a rich grade-level paragraph and write full sentence answers.",
        "prerequisites": ["g1_reading_passage_1"],
        "icon": "🌳",
        "order": 28
    },
    {
        "id": "g2_math_double_digit",
        "grade": GradeLevel.GRADE2,
        "domain": SkillDomain.NUMERACY,
        "title": "Double-Digit Math: Column Addition",
        "description": "Solve vertical 2-digit addition problems (e.g. 24 + 13 = 37).",
        "prerequisites": ["g1_math_addition_20", "g1_math_place_value"],
        "icon": "🧮",
        "order": 29
    },
    {
        "id": "g2_intro_multiplication",
        "grade": GradeLevel.GRADE2,
        "domain": SkillDomain.NUMERACY,
        "title": "Array Magic: Intro to Multiplication",
        "description": "Count equal groups and rows of items (e.g. 3 rows of 4 stars = 12).",
        "prerequisites": ["g2_math_double_digit"],
        "icon": "✨",
        "order": 30
    }
]

# Standard Lesson Content Template Store
LESSON_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "jk_trace_straight_lines": {
        "title": "Pre-Writing: Straight Road Lines",
        "subtitle": "Help the little car reach the finish line!",
        "description": "Practice holding pencil and tracing straight vertical, horizontal, and slanted lines.",
        "difficulty": 1,
        "instructions_for_child": "Start at the star 🌟 and trace along the dotted line all the way to the flag 🏁 without lifting your pencil!",
        "instructions_for_parent": "Encourage a relaxed pincer grasp. Celebrate smooth, continuous lines even if slightly wobbly.",
        "target_objectives": ["Fine motor pencil control", "Top-to-bottom and left-to-right tracking"],
        "exercises": [
            {
                "id": "ex1",
                "type": "trace_line",
                "prompt": "Trace down from the star to the apple!",
                "data": {"style": "vertical", "count": 4, "start_icon": "⭐", "end_icon": "🍎", "dashed": True}
            },
            {
                "id": "ex2",
                "type": "trace_line",
                "prompt": "Trace across from the bunny to the carrot!",
                "data": {"style": "horizontal", "count": 4, "start_icon": "🐰", "end_icon": "🥕", "dashed": True}
            },
            {
                "id": "ex3",
                "type": "trace_line",
                "prompt": "Trace the slide from top to bottom!",
                "data": {"style": "diagonal", "count": 4, "start_icon": "🎈", "end_icon": "🎪", "dashed": True}
            }
        ]
    },
    "jk_trace_curves_waves": {
        "title": "Fine Motor: Ocean Waves & Loops",
        "subtitle": "Sail the boat across the wavy sea!",
        "description": "Trace wavy curves, rainbow arcs, and zig-zag mountain peaks.",
        "difficulty": 1,
        "instructions_for_child": "Put your pencil on the little fish 🐟 and follow the gentle waves to the treasure chest 💎!",
        "instructions_for_parent": "Remind your child to take their time along the curves.",
        "target_objectives": ["Curvilinear pencil control", "Hand-eye coordination"],
        "exercises": [
            {
                "id": "ex1",
                "type": "trace_line",
                "prompt": "Trace the gentle ocean waves!",
                "data": {"style": "wave", "count": 3, "start_icon": "⛵", "end_icon": "🏝️", "dashed": True}
            },
            {
                "id": "ex2",
                "type": "trace_line",
                "prompt": "Hop over the mountain peaks with the goat!",
                "data": {"style": "zigzag", "count": 3, "start_icon": "🐐", "end_icon": "🏔️", "dashed": True}
            },
            {
                "id": "ex3",
                "type": "trace_line",
                "prompt": "Trace the bouncy loops of the bumblebee!",
                "data": {"style": "loops", "count": 2, "start_icon": "🐝", "end_icon": "🌸", "dashed": True}
            }
        ]
    },
    "jk_letter_a_d": {
        "title": "Alphabet Safari: Letters A, B, C, D",
        "subtitle": "Trace uppercase and lowercase letters and discover animal friends!",
        "description": "Practice stroke directions for A, B, C, D and associate with initial sounds.",
        "difficulty": 1,
        "instructions_for_child": "Trace the big and small letters. Then color the picture that matches the sound!",
        "instructions_for_parent": "Say the letter sound together: /a/ as in Alligator, /b/ as in Bear, /c/ as in Cat, /d/ as in Duck.",
        "target_objectives": ["Letter formation for A-D", "Initial phoneme identification"],
        "exercises": [
            {
                "id": "ex_a",
                "type": "trace_letter",
                "prompt": "Letter A: A is for Alligator! Trace Aa.",
                "data": {"upper": "A", "lower": "a", "sound_word": "Alligator", "icon": "🐊", "samples": ["A A A", "a a a", "Aa Aa"]}
            },
            {
                "id": "ex_b",
                "type": "trace_letter",
                "prompt": "Letter B: B is for Bear! Trace Bb.",
                "data": {"upper": "B", "lower": "b", "sound_word": "Bear", "icon": "🐻", "samples": ["B B B", "b b b", "Bb Bb"]}
            },
            {
                "id": "ex_c",
                "type": "trace_letter",
                "prompt": "Letter C: C is for Cat! Trace Cc.",
                "data": {"upper": "C", "lower": "c", "sound_word": "Cat", "icon": "🐱", "samples": ["C C C", "c c c", "Cc Cc"]}
            },
            {
                "id": "ex_d",
                "type": "trace_letter",
                "prompt": "Letter D: D is for Duck! Trace Dd.",
                "data": {"upper": "D", "lower": "d", "sound_word": "Duck", "icon": "🦆", "samples": ["D D D", "d d d", "Dd Dd"]}
            }
        ]
    },
    "jk_numbers_1_5": {
        "title": "Number Garden: Counting & Tracing 1 to 5",
        "subtitle": "Count cute butterflies and trace your numbers!",
        "description": "Trace numerals 1 to 5 and match with counted quantities.",
        "difficulty": 1,
        "instructions_for_child": "Count how many items there are in each row, then trace the number!",
        "instructions_for_parent": "Have your child touch each picture as they count out loud (1-to-1 correspondence).",
        "target_objectives": ["Number recognition 1-5", "One-to-one counting correspondence"],
        "exercises": [
            {
                "id": "num_1",
                "type": "count_items",
                "prompt": "Count the shining sun! Trace the number 1.",
                "data": {"target_count": 1, "item_icon": "☀️", "numeral": "1", "trace_samples": ["1", "1", "1", "1"]}
            },
            {
                "id": "num_2",
                "type": "count_items",
                "prompt": "Count the friendly pandas! Trace the number 2.",
                "data": {"target_count": 2, "item_icon": "🐼", "numeral": "2", "trace_samples": ["2", "2", "2", "2"]}
            },
            {
                "id": "num_3",
                "type": "count_items",
                "prompt": "Count the delicious strawberries! Trace the number 3.",
                "data": {"target_count": 3, "item_icon": "🍓", "numeral": "3", "trace_samples": ["3", "3", "3", "3"]}
            },
            {
                "id": "num_4",
                "type": "count_items",
                "prompt": "Count the flying rockets! Trace the number 4.",
                "data": {"target_count": 4, "item_icon": "🚀", "numeral": "4", "trace_samples": ["4", "4", "4", "4"]}
            },
            {
                "id": "num_5",
                "type": "count_items",
                "prompt": "Count the bright stars! Trace the number 5.",
                "data": {"target_count": 5, "item_icon": "⭐", "numeral": "5", "trace_samples": ["5", "5", "5", "5"]}
            }
        ]
    },
    "jk_shapes_basic": {
        "title": "Shape Detective: Circle, Square, Triangle, Star",
        "subtitle": "Trace each shape and color it in!",
        "description": "Practice tracing 2D shapes with stroke guidelines.",
        "difficulty": 1,
        "instructions_for_child": "Trace around each shape. Then draw your favorite face inside the circle!",
        "instructions_for_parent": "Talk about the number of sides each shape has (Circle = 0 curved, Triangle = 3 straight, Square = 4 equal).",
        "target_objectives": ["Shape recognition and spatial naming", "Continuous boundary line tracing"],
        "exercises": [
            {
                "id": "shape_circle",
                "type": "trace_shape",
                "prompt": "Trace the round Circle (0 corners)!",
                "data": {"shape": "circle", "name": "Circle", "icon": "⭕", "sides": 0}
            },
            {
                "id": "shape_square",
                "type": "trace_shape",
                "prompt": "Trace the Square with 4 straight sides!",
                "data": {"shape": "square", "name": "Square", "icon": "🟦", "sides": 4}
            },
            {
                "id": "shape_triangle",
                "type": "trace_shape",
                "prompt": "Trace the Triangle with 3 pointy corners!",
                "data": {"shape": "triangle", "name": "Triangle", "icon": "🔺", "sides": 3}
            },
            {
                "id": "shape_star",
                "type": "trace_shape",
                "prompt": "Trace the 5-point Star!",
                "data": {"shape": "star", "name": "Star", "icon": "⭐", "sides": 5}
            }
        ]
    },
    "jk_patterns_ab": {
        "title": "Pattern Magic: Simple AB Sequences",
        "subtitle": "What comes next in the line?",
        "description": "Identify repeating AB patterns and circle or draw the missing next object.",
        "difficulty": 1,
        "instructions_for_child": "Say the pattern out loud: 'Apple, Banana, Apple, Banana...' What comes next? Circle the right one!",
        "instructions_for_parent": "Chanting the pattern rhythmically helps children develop algebraic thinking.",
        "target_objectives": ["Pattern recognition", "Logical sequencing"],
        "exercises": [
            {
                "id": "pat_1",
                "type": "fill_pattern",
                "prompt": "Apple, Banana, Apple, Banana... What is next?",
                "data": {
                    "sequence": ["🍎", "🍌", "🍎", "🍌"],
                    "choices": ["🍎", "🍌", "🍇"],
                    "answer": "🍎"
                }
            },
            {
                "id": "pat_2",
                "type": "fill_pattern",
                "prompt": "Cat, Dog, Cat, Dog... What is next?",
                "data": {
                    "sequence": ["🐱", "🐶", "🐱", "🐶"],
                    "choices": ["🐱", "🐶", "🐰"],
                    "answer": "🐱"
                }
            },
            {
                "id": "pat_3",
                "type": "fill_pattern",
                "prompt": "Sun, Moon, Sun, Moon... What is next?",
                "data": {
                    "sequence": ["☀️", "🌙", "☀️", "🌙"],
                    "choices": ["☀️", "🌙", "⭐"],
                    "answer": "☀️"
                }
            }
        ]
    },
    "sk_cvc_short_a": {
        "title": "Word Builder: Short 'a' CVC Words",
        "subtitle": "Sound out and write 3-letter words!",
        "description": "Decode initial consonant, short 'a', and final consonant to spell words.",
        "difficulty": 2,
        "instructions_for_child": "Look at the picture. Say the sounds /c/ - /a/ - /t/. Write each letter in the sound box!",
        "instructions_for_parent": "Encourage tapping out the 3 distinct sounds before writing.",
        "target_objectives": ["Phoneme segmentation", "Early 3-letter spelling"],
        "exercises": [
            {
                "id": "cvc_cat",
                "type": "cvc_box",
                "prompt": "Spell the word: C - A - T (Cat)",
                "data": {"word": "CAT", "letters": ["C", "A", "T"], "icon": "🐱", "trace_guide": "c a t"}
            },
            {
                "id": "cvc_hat",
                "type": "cvc_box",
                "prompt": "Spell the word: H - A - T (Hat)",
                "data": {"word": "HAT", "letters": ["H", "A", "T"], "icon": "🎩", "trace_guide": "h a t"}
            },
            {
                "id": "cvc_bat",
                "type": "cvc_box",
                "prompt": "Spell the word: B - A - T (Bat)",
                "data": {"word": "BAT", "letters": ["B", "A", "T"], "icon": "🦇", "trace_guide": "b a t"}
            },
            {
                "id": "cvc_map",
                "type": "cvc_box",
                "prompt": "Spell the word: M - A - P (Map)",
                "data": {"word": "MAP", "letters": ["M", "A", "P"], "icon": "🗺️", "trace_guide": "m a p"}
            }
        ]
    },
    "sk_addition_to_5": {
        "title": "Picture Addition: Sums up to 5",
        "subtitle": "Count and add the objects together!",
        "description": "Add two groups of objects with visual icons.",
        "difficulty": 2,
        "instructions_for_child": "Count the first group, then count the second group. How many in all? Write your answer in the box!",
        "instructions_for_parent": "Use fingers or small counters (like beans or pennies) to physically verify each sum.",
        "target_objectives": ["Conceptual understanding of addition as joining groups", "Writing numerals 1-5"],
        "exercises": [
            {
                "id": "add_1",
                "type": "math_problem",
                "prompt": "2 Fish + 1 Fish = How many fish?",
                "data": {"operand1": 2, "operand2": 1, "operator": "+", "answer": 3, "icon": "🐟", "group1": "🐟🐟", "group2": "🐟"}
            },
            {
                "id": "add_2",
                "type": "math_problem",
                "prompt": "3 Apples + 2 Apples = How many apples?",
                "data": {"operand1": 3, "operand2": 2, "operator": "+", "answer": 5, "icon": "🍎", "group1": "🍎🍎🍎", "group2": "🍎🍎"}
            },
            {
                "id": "add_3",
                "type": "math_problem",
                "prompt": "1 Star + 3 Stars = How many stars?",
                "data": {"operand1": 1, "operand2": 3, "operator": "+", "answer": 4, "icon": "⭐", "group1": "⭐", "group2": "⭐⭐⭐"}
            }
        ]
    },
    "g1_reading_passage_1": {
        "title": "Story Time: The Friendly Puppy",
        "subtitle": "Read the story and answer 3 questions!",
        "description": "Beginning reader decodable story with simple comprehension questions.",
        "difficulty": 3,
        "instructions_for_child": "Read the short story out loud. Then circle the right answer for each question!",
        "instructions_for_parent": "Point to each word as your child reads. Support with unfamiliar words.",
        "target_objectives": ["Reading fluency", "Literal reading comprehension"],
        "exercises": [
            {
                "id": "story_text",
                "type": "reading_passage",
                "prompt": "Read the story below:",
                "data": {
                    "passage": "Max is a little brown puppy. Max loves to run in the green park. He has a red bouncy ball. Max can jump high to catch his ball!",
                    "questions": [
                        {"q": "What kind of animal is Max?", "options": ["A kitten", "A puppy", "A rabbit"], "answer": "A puppy"},
                        {"q": "Where does Max love to run?", "options": ["In the park", "In the pool", "In the school"], "answer": "In the park"},
                        {"q": "What color is Max's ball?", "options": ["Blue", "Yellow", "Red"], "answer": "Red"}
                    ]
                }
            }
        ]
    }
}

def get_all_curriculum_nodes() -> List[Dict[str, Any]]:
    return CURRICULUM_SKILLS

def get_skill_by_id(skill_id: str) -> Optional[Dict[str, Any]]:
    for skill in CURRICULUM_SKILLS:
        if skill["id"] == skill_id:
            return skill
    return None

def get_lesson_plan(lesson_id: str) -> Optional[LessonPlan]:
    skill = get_skill_by_id(lesson_id)
    if not skill:
        return None
    
    template = LESSON_TEMPLATES.get(lesson_id)
    if template:
        exercises = [ExerciseItem(**ex) for ex in template.get("exercises", [])]
        return LessonPlan(
            id=lesson_id,
            grade=skill["grade"],
            domain=skill["domain"],
            skill_id=lesson_id,
            title=template["title"],
            subtitle=template["subtitle"],
            description=template["description"],
            difficulty=template.get("difficulty", 1),
            instructions_for_child=template["instructions_for_child"],
            instructions_for_parent=template["instructions_for_parent"],
            target_objectives=template["target_objectives"],
            exercises=exercises
        )
    
    # Fallback default template if not explicitly predefined
    return LessonPlan(
        id=lesson_id,
        grade=skill["grade"],
        domain=skill["domain"],
        skill_id=lesson_id,
        title=skill["title"],
        subtitle=f"Master {skill['title']}",
        description=skill["description"],
        difficulty=1,
        instructions_for_child=f"Follow the instructions to complete your {skill['title']} worksheet!",
        instructions_for_parent="Guide your child gently and encourage them to try each question.",
        target_objectives=[skill["title"], f"{skill['grade']} milestone"],
        exercises=[
            ExerciseItem(
                id="default_ex1",
                type="trace_line",
                prompt=f"Practice {skill['title']}",
                data={"style": "horizontal", "count": 3, "start_icon": skill.get("icon", "⭐"), "end_icon": "🏁"}
            )
        ]
    )

def compute_skills_status(mastered_skill_ids: List[str], current_grade: GradeLevel) -> Dict[str, Dict[str, Any]]:
    status_map = {}
    mastered_set = set(mastered_skill_ids)
    
    for skill in CURRICULUM_SKILLS:
        sid = skill["id"]
        prereqs = skill["prerequisites"]
        
        if sid in mastered_set:
            status = "mastered"
        elif not prereqs or all(p in mastered_set for p in prereqs):
            status = "available"
        else:
            status = "locked"
            
        status_map[sid] = {
            **skill,
            "status": status,
            "is_current_grade": skill["grade"] == current_grade
        }
    return status_map
