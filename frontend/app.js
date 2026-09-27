let language="";
let session_id=Math.random().toString(36).substring(2);

const API=window.location.origin+"/proxy/5000";



function selectLanguage(lang,button){

    language=lang;

    document.querySelectorAll(".languages button")
    .forEach(btn=>btn.classList.remove("selected"));

    button.classList.add("selected");


    let name=
    lang==="arabic"?"Arabic / العربية":
    lang==="english"?"English / الإنجليزية":
    "Mixed / مزدوج";


    let role=document.getElementById("job_role").value;


    document.getElementById("selected").innerText=
    "Selected: "+name+" | "+role;

}





async function startInterview(){

    let role=document.getElementById("job_role").value;


    console.log(
        "START",
        language,
        role,
        session_id
    );


    if(!language){

        alert("Choose language first");
        return;

    }



    document.getElementById("setup")
    .classList.add("hidden");


    document.getElementById("chat")
    .classList.remove("hidden");



    try{

        let response=await fetch(API+"/start",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                language:language,

                job_role:role,

                session_id:session_id

            })

        });


        let data=await response.json();


        addMessage(
            "AI Interviewer",
            data.message,
            "ai"
        );


    }catch(error){

        console.error(error);

        addMessage(
            "AI Interviewer",
            "Server connection failed.",
            "ai"
        );

    }

}







async function sendAnswer(){

    let input=document.getElementById("answer");

    let text=input.value.trim();


    if(!text)return;



    addMessage(
        "You",
        text,
        "user"
    );


    input.value="";



    try{


        let response=await fetch(API+"/answer",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                session_id:session_id,

                answer:text

            })

        });



        let data=await response.json();



        console.log("AI RESPONSE:",data.message);



        try{


            let clean=data.message
            .replace(/```json/g,"")
            .replace(/```/g,"")
            .trim();


            let feedback=JSON.parse(clean);


            showFeedback(feedback);



        }catch(error){


            console.log(
                "Feedback Parse Error:",
                error
            );


            addMessage(
                "AI Interviewer",
                data.message,
                "ai"
            );

        }



    }catch(error){


        console.error(error);


        addMessage(
            "AI Interviewer",
            "Server connection failed.",
            "ai"
        );

    }

}








function showFeedback(data){


    document.getElementById("chat")
    .classList.add("hidden");


    document.getElementById("feedback")
    .classList.remove("hidden");



    let strengths=document.getElementById("strengths");

    strengths.innerHTML="";


    data.strengths.forEach(item=>{

        strengths.innerHTML+=`
        <li>${item}</li>
        `;

    });



    let improvements=document.getElementById("improvements");

    improvements.innerHTML="";


    data.improvements.forEach(item=>{

        improvements.innerHTML+=`
        <li>${item}</li>
        `;

    });



    document.getElementById("technical").innerText=
    data.technical_knowledge || "";


    document.getElementById("communication").innerText=
    data.communication || "";


    document.getElementById("problem_solving").innerText=
    data.problem_solving || "";


    document.getElementById("summary").innerText=
    data.summary || "";

}







function addMessage(sender,text,type){

    let box=document.getElementById("messages");


    let direction=
    (language==="arabic"||language==="mixed")
    ?"rtl":"ltr";


    box.innerHTML+=`

    <div class="message ${type}" style="direction:${direction}">

        <b>${sender}</b>

        <p>${text}</p>

    </div>

    `;


    box.scrollTop=box.scrollHeight;

}