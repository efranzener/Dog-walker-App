import React from 'react';

function SitterSignup() {

    const formInputs = {
        // type: document.querySelector('#type-field').value,
        // amount: document.querySelector('#amount-field').value,
        "fname": "Ety",
        "lname": "Franzener"
      };

    function handleSignup() {
        fetch("http://127.0.0.1:5000/sitter-signup", {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',
            },
          }).then(function (response) {
            console.log("response:", response);
          }).catch(function (error) {
            console.log("error:", error);
          });
    }

  return (
    <div className="signup">
        <form>
            <label>
                First name:
                <input type="text" name="fname" />
            </label>
            <label>
                Last name:
                <input type="text" name="lname" />
            </label>
            <input type="submit" value="Submit" onClick={handleSignup} />
        </form>
    
    </div>  
  );

}

export default SitterSignup;