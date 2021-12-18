# indian_banks
A REST service that can:

Given a bank branch IFSC code, get bank details
Given a bank name and city, gets details of all branches of the bank in the city

# To register a new user- POST method
http://localhost:5000/api/auth/register
pass parameters->  {
                      "email":"eamil",
                      "password":"password",
                      "confirm_password":"password"
                   }

# To login a registered user- POST method
http://localhost:5000/api/auth/login
pass parameters-> {
                    "email":"email",
                     "password":"password"
                  }
                  
jwt token will be generated that will be valid for 5 days--> pass that generated token in x-access-tokens in request.headers

# To get bank details using bank IFSC code 
http://localhost:5000/ifsc/<ifsc>

  For e.g.
  If IFSC is ABHY0065001, then -> http://localhost:5000/ifsc/ABHY0065001
  
  Output->
  {
    "branch_details": [
        {
            "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
            "bank_id": 60,
            "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
            "branch": "RTGS-HO",
            "city": "MUMBAI",
            "district": "GREATER MUMBAI",
            "ifsc": "ABHY0065001",
            "index": 0,
            "state": "MAHARASHTRA"
        }
    ]
}
  
# To get bank branches deatils using bank name and bank city
  http://localhost:5000/bank_name/<bank_name>/city/<city>
  
    For e.g.
     If bank name is ABHYUDAYA COOPERATIVE BANK LIMITED and city is MUMBAI , then -> http://localhost:5000/bank_name/ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED/city/MUMBAI
  
  Output ->
  {
    "branch_details": [
        {
            "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
            "bank_id": 60,
            "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
            "branch": "RTGS-HO",
            "city": "MUMBAI",
            "district": "GREATER MUMBAI",
            "ifsc": "ABHY0065001",
            "index": 0,
            "state": "MAHARASHTRA"
        },
        {
            "address": "ABHYUDAYA EDUCATION SOCIETY, OPP. BLDG. NO. 18, ABHYUDAYA NAGAR, KALACHOWKY, MUMBAI - 400033",
            "bank_id": 60,
            "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
            "branch": "ABHYUDAYA NAGAR",
            "city": "MUMBAI",
            "district": "GREATER MUMBAI",
            "ifsc": "ABHY0065002",
            "index": 1,
            "state": "MAHARASHTRA"
        }
  
By defalut, offset is set to 0 and limit is 100, to change the offset and limit you need to pass the limit and offset in url
For e.g.
http://localhost:5000/bank_name/ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED/city/MUMBAI?offset=0&limit=2