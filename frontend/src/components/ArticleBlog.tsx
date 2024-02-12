import { useNavigate } from "react-router";
type props = {
    id:number,
    title:string, 
    mdate:string,
    img_url:string,
}

const ArticleBlog = ({id, title, mdate, img_url}:props) => {

    const navigate = useNavigate();

    const handleViewDetails = () => {
        navigate(`/articles/:${id}`);
    }

    return(
        <>
            <div className="w-full relative cursor-pointer" onClick={handleViewDetails}>
                <div className="overflow-hidden h-[250px]"><img src={img_url} className="hover:scale-110 duration-500"></img></div>
                <div className="absolute w-[80%] bottom-[-40px] bg-white text-black p-2">
                    <p className=" text-gray-400 text-xs pb-2">{mdate}</p>
                    <p className="font-sans text-[19px] font-medium">
                        {title}
                    </p>
                </div>
            </div>
        </>
    )
}

export default ArticleBlog;