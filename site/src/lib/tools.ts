import fs from 'fs';
import path from 'path';
import toolsData from '@/data/tools.json';

export interface Tool {
    number: string;
    name: string;
    category: string;
    short_description: string;
    practical_exercise: string;
    ios_app: string;
    detailed_description: string;
    implementation_strategy: string;
    sort_num: number;
    slug: string;
}

export function getTools(): Tool[] {
    return toolsData.map((tool: any) => ({
        ...tool,
        slug: tool.name.toLowerCase().replace(/[\W_]+/g, '-').replace(/^-+|-+$/g, ''),
    }));
}

export function getToolBySlug(slug: string): Tool | undefined {
    const tools = getTools();
    return tools.find((t) => t.slug === slug);
}

export function getToolContent(slug: string): string | null {
    const contentPath = path.join(process.cwd(), 'content', `${slug}.md`);
    try {
        return fs.readFileSync(contentPath, 'utf8');
    } catch (error) {
        console.error(`Error reading file for slug ${slug}:`, error);
        return null;
    }
}
