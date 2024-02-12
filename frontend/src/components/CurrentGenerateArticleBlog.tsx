
type props = {
    id:number,
    title: string,
    summary: string,
    mdate: string,
    img_url: string,
}

const CurrentGenerateArticleBlog = ({id,title, summary, mdate, img_url}:props) => {

    const handleViewDetails = () => {
        window.location.href= `/articles/:${id}`;
    }

    return(
        <>
            <div className="w-full relative cursor-pointer" onClick={handleViewDetails}>
                <div className="overflow-hidden h-[500px]"><img src={img_url} className="w-[100%]  hover:scale-110 duration-500"></img></div>
                <div className="absolute w-[80%] bottom-[-80px] bg-white text-black p-2">
                    <p className=" text-gray-400 text-xs pb-2">Popular | {mdate}</p>
                    <p className="font-sans text-2xl font-medium">
                        {title}
                    </p>
                    <div className="font-sans text-[18px] pt-2 h-[68px] overflow-hidden">
                        {summary}
                    </div>
                    <p className="font-sans text-base pt-2 text-primary">Read More</p>
                </div>
            </div>
        </>
    )
}

export default CurrentGenerateArticleBlog;