document.addEventListener('DOMContentLoaded',()=>{
   
    let edit_btns = document.querySelectorAll('.edit_btn')

    edit_btns.forEach((btn)=>{
        btn.addEventListener('click', event =>{

            const el_btn = event.target
            let post_id = el_btn.value
            
            let target =  el_btn.parentElement.parentElement.querySelector('.post_body')
            let old = target.innerHTML

            target.innerHTML =`<textarea class="new_body">${old}</textarea><button class="save_btn btn btn-outline-success">Save</button>`
            let save_btn = target.querySelector('.save_btn')
           
            let btn_element = event.target
            el_btn.remove()
           
            save_btn.addEventListener('click',event =>{
                let save = event.target
                let new_content = save.parentElement.parentElement.querySelector('.new_body').value
                save.parentElement.parentElement.append(btn_element)
                edit(post_id,new_content);
                target.innerHTML =  new_content

            })
            

        })
    })


})
    


function add_post(){
    let new_post = document.querySelector('#form_body').value
    // fetch the create view function 
    fetch('/newpost',{
        //send the request using the POST method 
        method:'POST',
        //send the data to the function in the body after stringify it 
        body: JSON.stringify({    
        post: new_post
    })
 })
 
   //loading the home content after receiving the promise to get the latest task entered
    .then(result => {
        console.log(result);
        this.location.reload();
    });

    return false;
}

function follow_manage(target_id){
    let id = `${target_id}` 
    const f_btn = document.querySelector('#follow_un')
    if(f_btn.innerHTML === 'Unfollow'){

        f_btn.innerHTML = 'Follow'
        f_btn.value = id
        f_btn.setAttribute("class", "btn btn-outline-primary")

        fetch(`/follow_feature/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                unfollow: 'yes'
            })
          })
          .then(response => response.json())
          .then(result => {
                console.log(result);
            }); 

    }
    else if (f_btn.innerHTML ==='Follow'){

        f_btn.innerHTML = 'Unfollow'
        f_btn.value = id
        f_btn.setAttribute("class", "btn btn-outline-danger")

        fetch(`/follow_feature/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: 'yes'
            })
          })
          .then(response => response.json())
          .then(result => {
                console.log(result);
            }); 


    }
}


function edit(id,newcontent){
    fetch(`/edit`, {
        method: 'PUT',
        body: JSON.stringify({
            target_id: id,
            content: newcontent
        })
      })
      .then(response => response.json())
      .then(result => {
            console.log(result);
        }); 

}
  

async function like(like){
    let target_like = like.parentElement.parentElement.parentElement.querySelector('.like_c')
    let id = like.getAttribute("data-id")
 
    like.setAttribute('onclick','unlike(this)')
    let response = await fetch(`/like_feature`, {
        method: 'PUT',
        body: JSON.stringify({
            target_id: id,
            like: 'yes'
        })
      })
    let new_like = await response.json()

    target_like.innerHTML=new_like.total_likes

}

async function unlike(like){
    let target_like = like.parentElement.parentElement.parentElement.querySelector('.like_c')
    let id = like.getAttribute("data-id")
    
    like.setAttribute('onclick','like(this)')
    let response = await fetch(`/like_feature`, {
        method: 'PUT',
        body: JSON.stringify({
            target_id: id,
            unlike: 'yes'
        })
      })
    let new_like = await response.json()
    
    target_like.innerHTML=new_like.total_likes
        
}