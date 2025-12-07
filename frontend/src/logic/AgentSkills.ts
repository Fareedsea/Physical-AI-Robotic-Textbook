// Basic types for our Physical AI Agent System

export type SkillType = 'NAVIGATION' | 'MANIPULATION' | 'VISION' | 'COMMUNICATION';

export interface AgentSkill {
    id: string;
    name: string;
    type: SkillType;
    description: string;
    parameters: Record<string, string>; // e.g., { target: 'string', speed: 'number' }
    execute: (params: any) => Promise<boolean>;
}

export interface SubAgent {
    id: string;
    name: string;
    specialty: string;
    skills: string[]; // List of Skill IDs
    status: 'IDLE' | 'BUSY' | 'OFFLINE';
}

// Mock Registry of Skills
export const SKILL_REGISTRY: Record<string, AgentSkill> = {
    'nav_to': {
        id: 'nav_to',
        name: 'Navigate To',
        type: 'NAVIGATION',
        description: 'Moves the robot base to a specific coordinate or location label.',
        parameters: { target: 'string' },
        execute: async (params) => {
            console.log(`[Skill] Navigating to ${params.target}...`);
            await new Promise(r => setTimeout(r, 2000));
            return true;
        }
    },
    'pick_obj': {
        id: 'pick_obj',
        name: 'Pick Object',
        type: 'MANIPULATION',
        description: 'Uses the robotic arm to grasp an object.',
        parameters: { object_id: 'string' },
        execute: async (params) => {
            console.log(`[Skill] Picking up ${params.object_id}...`);
            await new Promise(r => setTimeout(r, 1500));
            return true;
        }
    },
    'scan_area': {
        id: 'scan_area',
        name: 'Scan Area',
        type: 'VISION',
        description: 'Rotates camera to detect objects.',
        parameters: { fov: 'number' },
        execute: async (params) => {
            console.log(`[Skill] Scanning area with FOV ${params.fov}...`);
            await new Promise(r => setTimeout(r, 1000));
            return true;
        }
    }
};

export const SUB_AGENTS: SubAgent[] = [
    {
        id: 'agent_nav',
        name: 'Navigator-1',
        specialty: 'Mobile Base Control',
        skills: ['nav_to'],
        status: 'IDLE'
    },
    {
        id: 'agent_arm',
        name: 'Manipulator-X',
        specialty: 'Arm Control',
        skills: ['pick_obj'],
        status: 'IDLE'
    },
    {
        id: 'agent_eye',
        name: 'Vision-Pro',
        specialty: 'Perception',
        skills: ['scan_area'],
        status: 'IDLE'
    }
];
