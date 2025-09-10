import re
import unidecode
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import nltk

# Download NLTK data (only once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize NLP components
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

# Tech stack normalization mappings
TECH_NORMALIZATION = {
    'react.js': 'react',
    'reactjs': 'react',
    'node.js': 'node',
    'nodejs': 'node',
    'vue.js': 'vue',
    'vuejs': 'vue',
    'angular.js': 'angular',
    'angularjs': 'angular',
    'express.js': 'express',
    'expressjs': 'express',
    'springboot': 'spring',
    'spring boot': 'spring',
    'spring framework': 'spring',
    'postgresql': 'postgres',
    'postgres db': 'postgres',
    'mongodb': 'mongo',
    'mysql': 'mysql',
    'sql server': 'sqlserver',
    'microsoft sql server': 'sqlserver',
    'aws': 'amazon web services',
    'azure': 'microsoft azure',
    'gcp': 'google cloud platform',
    'kubernetes': 'k8s',
    'docker': 'docker',
    'jenkins': 'jenkins',
    'git': 'git',
    'github': 'github',
    'gitlab': 'gitlab',
    'javascript': 'js',
    'typescript': 'ts',
    'python': 'python',
    'java': 'java',
    'c++': 'cpp',
    'c#': 'csharp',
    'ruby': 'ruby',
    'php': 'php',
    'html': 'html',
    'css': 'css',
    'sass': 'sass',
    'less': 'less',
    'webpack': 'webpack',
    'babel': 'babel',
    'redux': 'redux',
    'mobx': 'mobx',
    'graphql': 'graphql',
    'rest api': 'rest',
    'restful': 'rest'
}

# Common spelling variants
SPELLING_VARIANTS = {
    'ecommerce': 'e-commerce',
    'e commerce': 'e-commerce',
    'webapp': 'web application',
    'web app': 'web application',
    'microservice': 'microservices',
    'micro service': 'microservices',
    'apis': 'api',
    'databases': 'db',
    'database': 'db',
    'servers': 'server',
    'clients': 'client',
}

# Extra generic terms to ignore (beyond NLTK stopwords)
GENERIC_TERMS = {
    "engineering", "engineer", "highly", "seek", "skilled", 
    "join", "expertise", "motivated", "strong"
}

def preprocess_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""

    text = text.lower()
    text = unidecode.unidecode(text)  # normalize accents
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # URLs
    text = re.sub(r'\S+@\S+', '', text)  # Emails
    text = re.sub(r'[^a-zA-Z\s\-]', ' ', text)  # Remove special chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def handle_spelling_variants(text: str) -> str:
    words = text.split()
    normalized_words = []
    for word in words:
        word = SPELLING_VARIANTS.get(word, word)
        normalized_words.append(word)
    return ' '.join(normalized_words)

def remove_stopwords(text: str, keep_words=None) -> str:
    if keep_words is None:
        keep_words = set()
    words = text.split()
    return ' '.join([
        w for w in words 
        if (w not in stop_words and w not in GENERIC_TERMS) or w in keep_words
    ])

def lemmatize_text(text: str) -> str:
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

def normalize_tech_stack(text: str, keep_words=None) -> str:
    if not text or not isinstance(text, str):
        return ""

    # Step 1: Preprocess (clean text, remove URLs, emails, special chars, etc.)
    text = preprocess_text(text)

    # Step 2: Handle spelling variants
    text = handle_spelling_variants(text)

    # Step 3: Normalize tech stack terms
    tech_terms = list(TECH_NORMALIZATION.keys())
    tech_pattern = r'\b(' + '|'.join(re.escape(term) for term in tech_terms) + r')\b'

    def replace_tech(match):
        return TECH_NORMALIZATION.get(match.group(0).lower(), match.group(0))

    text = re.sub(tech_pattern, replace_tech, text, flags=re.IGNORECASE)

    # Step 4: Remove stopwords + generic filler terms
    text = remove_stopwords(text, keep_words=keep_words)

    # Step 5: Lemmatize text
    text = lemmatize_text(text)

    return text
