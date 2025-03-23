def get_extraction_prompt(page_content: str, url: str) -> str:
    """
    Generates a refined extraction prompt for the LLM based on the job listing content.
    
    The prompt instructs the LLM to extract the following fields:
      - company_name
      - position_title
      - location_type (remote/onsite/hybrid)
      - expected_salary_range
      - original_listing_url (should match the input URL)
      - required_skills (as a list)
      - functional_requirements
      - collaboration_timezone (if remote)
      - years_experience
      - posting_age (in days)
    """
    prompt = f"""
    You are an AI assistant specialized in extracting structured job listing information.
    Extract the following details from the provided job listing content and output in valid JSON format:
    - Company name
    - Position title
    - Location type (remote/onsite/hybrid)
    - Expected salary range
    - Original listing URL (should be the input URL)
    - Required skills (as a list)
    - Functional/business requirements
    - Collaboration timezone (if remote)
    - Years of experience required
    - Job posting age (in days since posted)
    
    The JSON output should have the following keys:
    "company_name", "position_title", "location_type", "expected_salary_range", "original_listing_url",
    "required_skills", "functional_requirements", "collaboration_timezone", "years_experience", "posting_age".
    
    Here is the job listing content:
    {page_content}
    
    Ensure the "original_listing_url" in the output is exactly: {url}
    """
    return prompt.strip()
