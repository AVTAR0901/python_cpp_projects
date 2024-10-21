import { useState } from "react";
import { useNavigate} from "react-router-dom";

const BASE_URL = 'http://localhost:8000/'

export const ProductsCreate= () => {
    const[name, setName] = useState('')
    const[price, setPrice] = useState('')
    const[quantity, setQuantity] = useState('')
    const navigate = useNavigate()

    const handleCreate = (event) => {
        event?.preventDefault()

        const json_string = JSON.stringify({name, price, quantity}) //here dictornary object is not created hence parameters name is same as api request name

        const responseOptions = {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: json_string
        }

        fetch(BASE_URL + 'product', responseOptions)
        .then(response => {
            if(response.ok){
                return response.json()
            }
            throw response
        })
        .then(data => {
            navigate('/')
        })
        .catch(error => {
            console.log(error);
        })
    }

    return(
        <div className="new_product body">
        <div className="new_product_title title">Create New Product</div>
        <div>
        <input className="input-1" placeholder="Name" 
        onChange={(event) => setName(event.target.value)}/>
        </div>
        <div>
        <input className="input-1" placeholder="Price" 
        onChange={(event) => setPrice(event.target.value)}/>
        </div>
        <div>
        <input className="input-1" placeholder="Quantity" 
        onChange={(event) => setQuantity(event.target.value)}/>
        </div>
        <button className="button-4" onClick={handleCreate}>Create Product</button>
        </div>
    )
}