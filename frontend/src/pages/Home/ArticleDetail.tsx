import { useEffect, useState } from "react";
import { useParams } from "react-router";
import axios from "axios";
import moment from "moment";
import { basic_url } from "@/stack/stack";
import parse from 'html-react-parser';
import "./ArticleDetail.css";
import SubscribeModal from "@/components/SubscribeModal";

interface DataItem {
    category_id: number,
    contents: string,
    created_at: Date,
    id: number,
    modified_at: Date,
    owner_id: number,
    rating: number,
    title: string
}


const ArticleDetail = () => {
    const id = useParams();
    const [detailData, setDetailData] = useState<DataItem | undefined>();
    const [subscribeVisible, setSubscribeVisible] = useState<boolean>(false);

    const handleSubscribe = () => {
        setSubscribeVisible(true);
    }

    useEffect(() => {
        if (id.id !== undefined) {
            const len = id.id.length;
            const st_id = id.id.slice(1, len);
            const num_id = Number(st_id);
            
            axios.get(`${basic_url}blogposts/${num_id}`).then((res) => {
                setDetailData(res.data);
            })
        }

    }, [])

    return (
        <>
            <div className="container">
                <div className="font-bold text-4xl mt-[100px] mb-3">
                    {
                        detailData?.title
                    }
                </div>
                <div className="text-xl text-black flex items-center">
                    <span className="pr-2">By :</span>
                    <span className="font-bold pr-2">GOLDEXCG.com</span>
                    <div className="w-10 h-10 rounded-[50%] overflow-hidden"><img src="/icons/1.png" className="w-10 h-10"></img></div>
                </div>
                <div className="text-[18px] text-gray-600 mb-3">
                    <span>Published: </span>
                    <span>
                        { 
                            moment(detailData?.created_at).format('YYYY/MM/DD kk:mm:ss ')
                        }
                        GMP-5
                    </span>
                </div>
                <hr className="pb-3"></hr>
                <div className="article-content">
                    {detailData !== undefined && parse(detailData.contents)}
                </div>
                <div className=" font-mono py-5 border-t border-b border-[#006F99] flex sm:flex-row flex-col justify-center items-center gap-5 my-10">
                    <p className="text-black text-base xl:text-xl text-center">Don't miss a thing! Sign up for a daily update delivered to your inbox</p>
                    <button className="w-[200px] h-[40px] text-base text-white bg-[#006F99]" onClick={() => handleSubscribe()}>Subscribe</button>
                </div>
                <SubscribeModal visible={subscribeVisible} setVisible={setSubscribeVisible}></SubscribeModal>
            </div>
        </>
    )
}

export default ArticleDetail;

