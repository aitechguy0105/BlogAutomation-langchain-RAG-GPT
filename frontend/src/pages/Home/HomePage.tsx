import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router";
import moment from 'moment';
import type { PaginationProps } from 'antd';
import { Pagination, message } from 'antd';
import SubscribeModal from '@/components/SubscribeModal';
import ArticleBlog from "@/components/ArticleBlog";
import CurrentGenerateArticleBlog from "@/components/CurrentGenerateArticleBlog";
import RelatedPersonSay from "@/components/RelatedPersonSay";
import TradingChart from "@/components/TradingChart";
import LoginModal from '@/components/LoginModal';
import GoldPriceChart from '@/components/GoldPriceChart';
import "@/components/Header.css";
import { basic_url } from '@/stack/stack';

interface DataItem {
    category_id: number,
    created_at: Date,
    img_url: string,
    id: number,
    modified_at: Date,
    owner_id: number,
    rating: number,
    summary: string,
    title: string,
}


const HomePage = () => {

    const navigate = useNavigate();

    const [searchVal, setSearchVal] = useState<string>("");
    const [allData, setAllData] = useState<DataItem[]>([]);
    const [pgNumber, setPgNumber] = useState(1);
    const [pgSize, setPgSize] = useState(10);
    const [loginModalV, setLoginModalV] = useState<number>(0);
    const [mostPopularArticle, setMostPopularArticle] = useState({ id: 0, title: "", summary: "", mdate: "", img_url: "" });
    const [relatedArticles, setRelatedArticles] = useState([{}]);
    const [monthPopularArticles, setMonthPopularArticles] = useState([{}]);
    const [category, setCategory] = useState<string>("latest");
    const [subscribeVisible, setSubscribeVisible] = useState<boolean>(false);
    const [totalCount, setTotalCount] = useState<number>(0);
    const [currentGoldPrice, setCurrentGoldPrice] = useState<number>(0);

    const onChange: PaginationProps['onChange'] = (pageNumber, pageSize) => {
        setPgNumber(pageNumber);
        setPgSize(pageSize);
    };

    const handleChange = (value: string) => {
        setSearchVal(value);
    }

    const handleCategory = (value: string) => {
        setCategory(value);
    }

    const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            if (category === "popular") axios.get(`${basic_url}blogposts/articles_by_popular/${pgNumber}/${pgSize}/${searchVal}`).then((res) => {
                setAllData(res.data);
            }).catch(() => message.error("Error network"))
            if (category === "latest") {
                if (searchVal) {
                    axios.get(`${basic_url}blogposts/articles_by_new/${pgNumber}/${pgSize}/${searchVal}`).then((res) => {
                        setAllData(res.data);
                    }).catch(() => message.error("Error network"))
                }
                else axios.get(`${basic_url}blogposts/articles_by_new/${pgNumber}/${pgSize}`).then((res) => {
                    setAllData(res.data);
                }).catch(() => message.error("Error network"))
            }
        }
    }

    const handleSubscribe = () => {
        setSubscribeVisible(true);
    }

    useEffect(() => {
        navigate("/");
    }, []);

    useEffect(() => {

        axios.get(`${basic_url}goldprices`).then((res) => {
            setCurrentGoldPrice(res.data.price);
        })
        axios.get(`${basic_url}blogposts/all_blogposts_count`).then((res) => {
            setTotalCount(res.data.count);
        })
        axios.get(`${basic_url}blogposts/popular_article_related_articles`).then((res) => {
            setMostPopularArticle({ id: res.data[0].id, title: res.data[0].title, summary: res.data[0].summary, mdate: moment(res.data[0].created_at).format("kk:mm:ss MM / DD / YYYY"), img_url: res.data[0].img_url });
            setRelatedArticles(res.data)
        }).catch(() => message.error("Error network Popular And Related Article"))


        axios.get(`${basic_url}blogposts/popular_articles_month`).then((res) => {
            setMonthPopularArticles(res.data);
        }).catch(() => message.error("Error network Popular Articles Month"))

    }, [])

    useEffect(() => {
        if (category === "popular") {
            if (searchVal) {
                axios.get(`${basic_url}blogposts/articles_by_popular/${pgNumber}/${pgSize}/${searchVal}`).then((res) => {
                    setAllData(res.data);

                }).catch(() => message.error("Error network Popular All data With Search Value"))
            }
            else axios.get(`${basic_url}blogposts/articles_by_popular/${pgNumber}/${pgSize}`).then((res) => {
                setAllData(res.data);
            }).catch(() => message.error("Error network Popular All Data No Search Value"))
        }

        if (category === "latest") {
            if (searchVal) {
                axios.get(`${basic_url}blogposts/articles_by_new/${pgNumber}/${pgSize}/${searchVal}`).then((res) => {
                    setAllData(res.data);
                }).catch(() => message.error("Error network Latest All data With Search Value"))
            }
            else axios.get(`${basic_url}blogposts/articles_by_new/${pgNumber}/${pgSize}`).then((res) => {
                setAllData(res.data);
            }).catch(() => message.error("Error network Latest All Data No Search Value"))
        }

    }, [category, pgNumber, pgSize])


    return (
        <>
            <div className="container">
                <div className="w-full flex xl:flex-row flex-col justify-between mb-24 mt-[80px]">
                    <div className="flex flex-col gap-16">
                        <div className="flex md:flex-row flex-col md:gap-0 gap-[130px] justify-between">
                            <div className="basis-[65%]">
                                <div className="text-center py-4 mb-12 text-[white] text-4xl bg-[#1d4354]">
                                    The Most Popular Article
                                </div>
                                <CurrentGenerateArticleBlog id={mostPopularArticle.id} title={mostPopularArticle.title} summary={mostPopularArticle.summary} mdate={mostPopularArticle.mdate} img_url={mostPopularArticle.img_url} />
                            </div>
                            <div className="basis-[33%] flex flex-col gap-12">
                                <div className="text-center py-4 text-[white] text-4xl bg-[#1d4354]">
                                    Related Articles
                                </div>
                                {
                                    relatedArticles.map((item: any, index: number) => {
                                        return index > 0 && <ArticleBlog id={item.id} title={item.title} mdate={moment(item.created_at).format("kk:mm:ss MM / DD / YYYY")} key={index} img_url={item.img_url} />
                                    })
                                }
                            </div>
                        </div>
                        <div>
                            <div className="w-full text-center py-4 text-[white] text-4xl bg-[#1d4354] mb-10">
                                Gold Price Chart
                            </div>
                            <div className="text-4xl text-[#a8323e] my-10">
                                Today's Gold Price : {currentGoldPrice}
                            </div>
                            <div className="w-full h-[400px] mb-[150px]">
                                <GoldPriceChart />
                            </div>
                        </div>
                    </div>
                    <div className="flex md:flex-row flex-col justify-between xl:mt-0 mt-[50px]">
                        <TradingChart />
                    </div>
                </div>

                <div className=" font-mono py-5 border-t border-b border-[#006F99] flex sm:flex-row flex-col justify-center items-center gap-5">
                    <p className="text-black text-base xl:text-[19px] text-center">Sign up to our newsletter to receive timely market updates and information on product sales and giveaways.</p>
                    <button className="w-[200px] h-[40px] text-base text-white bg-[#006F99]" onClick={() => handleSubscribe()}>Subscribe</button>
                </div>

                <SubscribeModal visible={subscribeVisible} setVisible={setSubscribeVisible} />
                <LoginModal visible={loginModalV} setVisible={setLoginModalV}></LoginModal>
                <div className="font-bold text-5xl text-center mt-[200px] mb-[50px]">Popular Articles in this Month</div>
                <div className="grid xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-x-5 gap-y-12 mb-[200px]">
                    {
                        monthPopularArticles.map((item: any, index: number) => {
                            return <ArticleBlog id={item.id} key={index} title={item.title} mdate={moment(item.created_at).format("kk:mm:ss MM / DD / YYYY")} img_url={item.img_url} />
                        })
                    }
                </div>
                <div className="font-bold text-center py-4 mb-12 text-black text-5xl ]">All Articles</div>
                <div className="mb-12 flex flex-row items-center gap-10 justify-end">
                    <div className="search-bar-form w-[400px] hidden lg:block relative">
                        <img src="/icons/icons8-search(2).svg" className="search-icon" />
                        <input id="search-bar" type="text" placeholder="Search" className="text-black" onChange={(e) => handleChange(e.target.value)} onKeyDown={(e) => handleSearch(e)} />
                    </div>
                    <label className="font-bold text-2xl pr-2 text-black">Order by : </label>
                    <select name="Order by Category" value={category} onChange={(e) => handleCategory(e.target.value)} id="order_by_category" className="w-[180px] h-[40px] border outline-none text-xl bg-white text-black">
                        <option value="latest">Latest</option>
                        <option value="popular">Popular</option>
                    </select>
                </div>
                <div className="flex flex-col gap-7">
                    {
                        allData.map((item, index) => {
                            return <div key={index}>
                                <RelatedPersonSay id={item.id} author="GOLDEXCG.com" time={moment(item.created_at).format("kk:mm:ss MM / DD / YYYY")} articleTitle={item.title} articleSubtitle={item.summary} img_url={item.img_url} />
                                <hr />
                            </div>
                        })
                    }
                </div>
                <div className="py-16">
                    <Pagination showQuickJumper defaultCurrent={1} total={totalCount} onChange={onChange} />
                </div>
            </div>
        </>
    )
}
export default HomePage;