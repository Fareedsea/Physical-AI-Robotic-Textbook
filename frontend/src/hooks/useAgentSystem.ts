import { useState, useCallback } from 'react';
import { AgentSkill, SubAgent, SKILL_REGISTRY, SUB_AGENTS } from '../logic/AgentSkills';

export function useAgentSystem() {
    const [subAgents, setSubAgents] = useState<SubAgent[]>(SUB_AGENTS);
    const [activeLogs, setActiveLogs] = useState<string[]>([]);
    const [isSystemBusy, setIsSystemBusy] = useState(false);

    const log = (msg: string) => {
        setActiveLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
    };

    const executeSkill = useCallback(async (skillId: string, params: any) => {
        const skill = SKILL_REGISTRY[skillId];
        if (!skill) {
            log(`Error: Skill ${skillId} not found.`);
            return { success: false, message: 'Skill not found' };
        }

        // Find capable agent
        // Note: In a real React state usage, reading 'subAgents' inside async callback might be stale if not careful.
        // But for this simple simulation, we will rely on current render scope or ref.
        // For safety, let's just assume we find one.

        // Simulating finding an agent
        const possibleAgents = SUB_AGENTS.filter(a => a.skills.includes(skillId));
        const agent = possibleAgents[0];

        if (!agent) {
            log(`Error: No agent capable of ${skill.name}.`);
            return { success: false, message: 'No agent found' };
        }

        setIsSystemBusy(true);
        log(`Assigning ${skill.name} to ${agent.name}...`);

        try {
            await skill.execute(params);
            log(`Success: ${skill.name} completed.`);
            setIsSystemBusy(false);
            return { success: true };
        } catch (e) {
            log(`Failure: ${skill.name} crashed.`);
            setIsSystemBusy(false);
            return { success: false };
        }
    }, []);

    return {
        subAgents,
        activeLogs,
        executeSkill,
        isSystemBusy,
        availableSkills: Object.values(SKILL_REGISTRY)
    };
}
