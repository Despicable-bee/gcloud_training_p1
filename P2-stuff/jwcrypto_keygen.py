from jwcrypto import jwk
import json
from datetime import date

print(" ---------------- Jwcrypto Key-pair generator ------------------------ ")
print(" Generating Key-pairs... ")
key = jwk.JWK.generate(kty="RSA", public_exponent=3, size=2048)

# Generate the JSON keys
public_key = json.loads(key.export_public())
private_key = json.loads(key.export_private())
public_key_container = { "keys": [] }

print(" Saving keys... ")
# Open up the files we're writing the JSON to.
privateKey_fileptr = open("cloud-training-PRIVATE-key.json", "w")
publicKey_fileptr = open("cloud-training-PUBLIC-key.json", "w")

today = str(date.today().strftime("%Y-%m-%d"))

# Add a couple of tags we need.
private_key['alg'] = 'RS256'
private_key['kid'] = today

public_key['alg'] = 'RS256'
public_key['kid'] = today

# Append the first key to the keys JSON list
public_key_container['keys'].append(public_key)

# Save the data
privateKey_fileptr.write(json.dumps(private_key, indent=4))
publicKey_fileptr.write(json.dumps(public_key_container, indent=4))

# Close the files because we're good boys :)
privateKey_fileptr.close()
publicKey_fileptr.close()
print(" Done! ")

