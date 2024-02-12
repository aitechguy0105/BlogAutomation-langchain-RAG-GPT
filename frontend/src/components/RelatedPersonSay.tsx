
type props = {
    id:number,
    author: string,
    time: string,
    articleTitle: string,
    articleSubtitle: string,
    img_url: string,
}

const RelatedPersonSay = ({ id,author, time, articleTitle, articleSubtitle, img_url }: props) => {

    const handleViewDetails = () => {
        window.location.href= `/articles/:${id}`;
    }

    return (
        <>
            <div className="flex xl:flex-row flex-col gap-8">
                {/*  */}
                <div className="basis-[25%] gap-10 flex flex-row overflow-hidden cursor-pointer" onClick={handleViewDetails}>
                    <div className="sm:basis-[50%] md:basis-[40%] lg:basis-[30%] xl:basis-[100%]"><img src={img_url} className="hover:scale-110 duration-700"></img></div>
                    <div className="hidden sm:basis-[30%] sm:flex sm:flex-col gap-5 xl:hidden">
                        <div className="w-[100px] h-[100px] rounded-[50%] overflow-hidden">
                            <img src="/icons/1.png" className="w-[100px] h-[100px]"></img>
                        </div>
                        <div className="flex flex-col justify-center gap-3">
                            <p className="font-bold text-[18px] text-black">{author}</p>
                            <p className="text-base text-gray-400">{time}</p>
                        </div>
                    </div>
                </div>
                <div className="basis-[75%] flex flex-col gap-8">
                    <div className="xl:flex xl:flex-row hidden gap-5">
                        <div className="w-[80px] h-[80px] rounded-[50%] overflow-hidden">
                            <img src="/icons/1.png" className="w-[80px] h-[80px]"></img>
                        </div>
                        <div className="flex flex-col justify-center gap-3">
                            <p className="font-bold text-[18px] text-black">{author}</p>
                            <p className="text-base text-gray-400">{time}</p>
                        </div>
                    </div>
                    <div className="flex flex-col gap-3 mb-3">
                            <p className="font-bold text-2xl text-black cursor-pointer" onClick={handleViewDetails}>{articleTitle}</p>
                            <div className="text-xl text-black h-[83px] overflow-hidden">{articleSubtitle}</div>
                            <p className="text-base text-primary cursor-pointer" onClick={handleViewDetails}>Read More</p>
                        </div>
                </div>

            </div>
        </>
    )
}

export default RelatedPersonSay;