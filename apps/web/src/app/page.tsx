"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Github, Cpu, Database, Network, Code, Layers, Zap, Info } from 'lucide-react';

export default function AetherDashboard() {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [repos, setRepos] = useState([
    { id: "1", name: "aether-core", language: "Rust", status: "Indexed", lastSync: "2h ago" },
    { id: "2", name: "distributed-db", language: "Go", status: "Indexing...", lastSync: "Now" },
    { id: "3", name: "frontend-monorepo", language: "TypeScript", status: "Indexed", lastSync: "1d ago" },
  ]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    setIsSearching(true);
    // Simulate search
    setTimeout(() => setIsSearching(false), 2000);
  };

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-12">
      {/* Header */}
      <header className="flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center shadow-[0_0_20px_rgba(168,85,247,0.4)]">
            <Cpu className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight neon-glow">AETHER <span className="text-primary">INTELLIGENCE</span></h1>
            <p className="text-xs text-muted-foreground uppercase tracking-widest">Enterprise Code OS</p>
          </div>
        </div>
        <div className="flex items-center space-x-6 text-sm">
          <div className="flex items-center space-x-2 text-green-400">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span>SYSTEM ONLINE</span>
          </div>
          <button className="bg-secondary px-4 py-2 rounded-lg border border-white/5 hover:border-white/20 transition-all">
            DOCUMENTATION
          </button>
        </div>
      </header>

      {/* Hero Search */}
      <section className="text-center space-y-8 py-12">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-4"
        >
          <h2 className="text-5xl font-extrabold tracking-tight">
            The Future of <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-400">Code Intelligence</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto font-light">
            Search, visualize, and reason about massive repositories using distributed semantic intelligence.
          </p>
        </motion.div>

        <form onSubmit={handleSearch} className="max-w-3xl mx-auto relative group">
          <div className="absolute inset-0 bg-primary/20 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-full"></div>
          <div className="relative flex items-center glass-card p-2">
            <Search className="ml-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Query repository architecture, business logic, or dependencies..."
              className="w-full bg-transparent border-none focus:ring-0 text-lg p-4 placeholder:text-muted-foreground/50"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button 
              type="submit"
              disabled={isSearching}
              className="bg-primary hover:bg-primary/90 text-white px-8 py-4 rounded-lg font-semibold transition-all disabled:opacity-50"
            >
              {isSearching ? "ANALYZING..." : "SEARCH"}
            </button>
          </div>
        </form>
      </section>

      {/* Grid Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: "Files Indexed", value: "1.2M+", icon: Code },
          { label: "Symbols Tracked", value: "45M+", icon: Network },
          { label: "Semantic Clusters", value: "842", icon: Database },
          { label: "Inference Time", value: "124ms", icon: Zap },
        ].map((stat, i) => (
          <div key={i} className="glass-card p-6 space-y-2">
            <div className="flex justify-between items-start">
              <stat.icon className="text-primary w-5 h-5" />
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Real-time</span>
            </div>
            <div>
              <p className="text-2xl font-bold">{stat.value}</p>
              <p className="text-xs text-muted-foreground">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Repositories Section */}
      <section className="space-y-6">
        <div className="flex justify-between items-end">
          <h3 className="text-xl font-semibold flex items-center space-x-2">
            <Github className="w-5 h-5" />
            <span>Active Repositories</span>
          </h3>
          <button className="text-primary text-sm font-medium hover:underline">View all assets</button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {repos.map((repo) => (
            <motion.div 
              key={repo.id}
              whileHover={{ scale: 1.02 }}
              className="glass-card p-6 space-y-4 cursor-pointer group"
            >
              <div className="flex justify-between items-start">
                <div className="p-3 bg-secondary rounded-xl group-hover:bg-primary/20 transition-colors">
                  <Layers className="w-6 h-6 text-primary" />
                </div>
                <div className="flex flex-col items-end">
                  <span className={`text-[10px] px-2 py-0.5 rounded-full ${repo.status === "Indexed" ? "bg-green-500/10 text-green-400" : "bg-yellow-500/10 text-yellow-400"}`}>
                    {repo.status}
                  </span>
                  <span className="text-[10px] text-muted-foreground mt-1">{repo.lastSync}</span>
                </div>
              </div>
              <div>
                <h4 className="text-lg font-bold group-hover:text-primary transition-colors">{repo.name}</h4>
                <p className="text-sm text-muted-foreground">{repo.language}</p>
              </div>
              <div className="pt-4 border-t border-white/5 flex justify-between items-center">
                <div className="flex -space-x-2">
                  {[1,2,3].map(i => (
                    <div key={i} className="w-6 h-6 rounded-full bg-secondary border border-background flex items-center justify-center text-[8px]">AI</div>
                  ))}
                </div>
                <button className="text-xs font-medium text-muted-foreground hover:text-white transition-colors">
                  EXPLORE ARCHITECTURE →
                </button>
              </div>
            </motion.div>
          ))}
          
          <div className="glass-card p-6 border-dashed border-white/20 flex flex-col items-center justify-center space-y-4 hover:border-primary/50 transition-colors cursor-pointer">
            <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center">
              <span className="text-2xl font-light text-muted-foreground">+</span>
            </div>
            <p className="text-sm text-muted-foreground font-medium">INGEST NEW REPOSITORY</p>
          </div>
        </div>
      </section>

      {/* Background Decor */}
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 -z-10 w-[800px] h-[800px] bg-primary/5 blur-[120px] rounded-full pointer-events-none"></div>
    </main>
  );
}
