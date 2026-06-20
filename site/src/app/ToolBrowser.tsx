'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import type { Tool } from '@/lib/tools';
import styles from './page.module.css';

export default function ToolBrowser({ tools }: { tools: Tool[] }) {
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  const categories = useMemo(
    () => Array.from(new Set(tools.map((t) => t.category))),
    [tools]
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return tools.filter((tool) => {
      const matchesCategory = !activeCategory || tool.category === activeCategory;
      if (!matchesCategory) return false;
      if (!q) return true;
      return (
        tool.name.toLowerCase().includes(q) ||
        tool.short_description.toLowerCase().includes(q) ||
        tool.category.toLowerCase().includes(q)
      );
    });
  }, [tools, query, activeCategory]);

  // Group the filtered tools by category, preserving original category order.
  const grouped = useMemo(() => {
    return categories
      .map((cat) => ({
        category: cat,
        tools: filtered.filter((t) => t.category === cat),
      }))
      .filter((group) => group.tools.length > 0);
  }, [categories, filtered]);

  return (
    <>
      <div className={styles.controls}>
        <input
          type="search"
          className={styles.search}
          placeholder="Search 77 tools by name or description…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Search thinking tools"
        />

        <div className={styles.filterRow}>
          <button
            type="button"
            className={`${styles.filterChip} ${activeCategory === null ? styles.filterChipActive : ''}`}
            onClick={() => setActiveCategory(null)}
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              type="button"
              key={cat}
              className={`${styles.filterChip} ${activeCategory === cat ? styles.filterChipActive : ''}`}
              onClick={() => setActiveCategory((prev) => (prev === cat ? null : cat))}
            >
              {cat}
            </button>
          ))}
        </div>

        <p className={styles.resultCount}>
          {filtered.length} {filtered.length === 1 ? 'tool' : 'tools'}
          {query.trim() ? ` matching “${query.trim()}”` : ''}
        </p>
      </div>

      <main className={styles.main}>
        {grouped.length === 0 ? (
          <p className={styles.empty}>No tools match your search.</p>
        ) : (
          grouped.map(({ category, tools: group }) => (
            <section key={category} className={styles.categorySection}>
              <h2 className={styles.categoryTitle}>{category}</h2>
              <div className={styles.grid}>
                {group.map((tool) => (
                  <Link href={`/tool/${tool.slug}`} key={tool.number} className={styles.cardLink}>
                    <div className={styles.card}>
                      <div className={styles.cardHeader}>
                        <span className={styles.toolNumber}>#{tool.number}</span>
                        <span className={styles.toolCategory}>{tool.category}</span>
                      </div>
                      <h3 className={styles.toolName}>{tool.name}</h3>
                      <p className={styles.toolDesc}>{tool.short_description}</p>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          ))
        )}
      </main>
    </>
  );
}
