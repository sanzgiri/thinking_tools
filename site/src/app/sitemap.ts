import type { MetadataRoute } from 'next';
import { getTools } from '@/lib/tools';

const SITE_URL = 'https://tools-for-thinking.netlify.app';

export default function sitemap(): MetadataRoute.Sitemap {
    const tools = getTools();

    const toolPages: MetadataRoute.Sitemap = tools.map((tool) => ({
        url: `${SITE_URL}/tool/${tool.slug}`,
        changeFrequency: 'monthly',
        priority: 0.8,
    }));

    return [
        {
            url: SITE_URL,
            changeFrequency: 'weekly',
            priority: 1,
        },
        ...toolPages,
    ];
}
