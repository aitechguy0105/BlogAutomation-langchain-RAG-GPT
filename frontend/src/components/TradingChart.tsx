import { useEffect } from 'react';

const TradingChart = () => {

    useEffect(() => {
        
    }, [])

    return (
        <>
            <div>
                <div className="text-center py-4 mb-12 text-[white] text-4xl" style={{ backgroundColor: 'rgb(29, 67, 84)' }}>
                    NEWS   
                </div>
                <div className="flex xl:flex-col md:flex-row md:gap-16 flex-col">
                    <iframe className="widget_preview_iframe" frameBorder="0" allow="autoplay; encrypted-media" allowFullScreen={true} scrolling="no" style={{visibility: "visible", width: "100%", height: "623px"}} src="https://www.feedspot.com/widgets/lookup/dea1Uv6h3f03"></iframe>
                    <iframe className="widget_preview_iframe" frameBorder="0" allow="autoplay; encrypted-media" allowFullScreen={true} scrolling="no" style={{visibility: "visible", width: "100%", height: "623px"}} src="https://www.feedspot.com/widgets/lookup/UvBgf648a2ac"></iframe>
                </div>
            </div>
        </>

    );
}

export default TradingChart;