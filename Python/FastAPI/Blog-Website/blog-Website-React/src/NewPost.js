import React, {useState} from "react";
import './NewPost.css'

const BASE_URL = 'http://localhost:8000/'

function NewPost(){
    const[image, setImage] = useState(null)
    const[creator, setCreator] = useState('')
    const[title, setTitle] = useState('')
    const[text, setText] = useState('')

    const handleImageUpload = (e) => {
        if(e.target.files[0]){
            setImage(e.target.files[0])
        }
    }

    const handleCreate = (e) => {
        e?.preventDefault()

        const formData = new FormData()
        formData.append('image', image)
        formData.append('title', title)
        formData.append('creator', creator)
        formData.append('content', text)

        const requestOptions = {
            method: 'POST',
            body: formData
        }
        fetch(BASE_URL + 'post', requestOptions)
        .then(response => {
            if (response.ok){
                return response.json()
            }
            throw response
        })
        .then(data => {
            window.location.reload()
            window.scrollTo(0, 0)
        })
        .catch(error => {
            console.log(error);
        })
        .finally(() => {
            setImage(null)
            document.getElementById('fileInput').value = null
        })
    }

    return(
        <div className="newpost_content">
        <div className="newpost_image">
        <input type="file" id="fileInput" onChange={handleImageUpload}/>
        </div>
        <div className="newpost_creator"> 
        <input className="newpost_creator" type="text" id="creator_input"
        placeholder="Creator" onChange={(event) => setCreator(event.target.value)}
        value={creator} />
        </div>
        <div className="newpost_title">
        <input className="newpost_title" type="text" id="title_input"
        placeholder="Title" onChange={(event) => setTitle(event.target.value)}
        value={title} />
        </div>
        <div className="newpost_text">
        <textarea className="newpost_text" rows='10' id="text_input"
        placeholder="text" onChange={(event) => setText(event.target.value)}
        value={text} />
        </div>
        <div>
        <button className="create_button" onClick={handleCreate}>Create </button>
        </div>
        </div>
    )

}

export default NewPost