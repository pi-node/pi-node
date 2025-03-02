// tests/unit/governance.test.js

const GovernanceService = require('../../src/services/governanceService'); // Adjust the path as necessary

describe('GovernanceService', () => {
    let governanceService;

    beforeEach(() => {
        governanceService = new GovernanceService();
    });

    test('should create a new proposal', () => {
        const proposal = governanceService.createProposal('Proposal Title', 'Proposal Description', 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        expect(proposal).toHaveProperty('id');
        expect(proposal).toHaveProperty('title', 'Proposal Title');
        expect(proposal).toHaveProperty('description', 'Proposal Description');
        expect(proposal).toHaveProperty('proposer', 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
    });

    test('should record a vote on a proposal', () => {
        const proposalId = 'mockProposalId';
        const vote = governanceService.voteOnProposal(proposalId, 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'yes');
        expect(vote).toHaveProperty('proposalId', proposalIdexpect(vote).toHaveProperty('voter', 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        expect(vote).toHaveProperty('choice', 'yes');
    });

    test('should throw an error if voting on a non-existent proposal', () => {
        const proposalId = 'nonExistentProposalId';
        expect(() => {
            governanceService.voteOnProposal(proposalId, 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'yes');
        }).toThrow('Proposal not found');
    });

    test('should return all proposals', () => {
        const proposals = governanceService.getAllProposals();
        expect(Array.isArray(proposals)).toBe(true);
    });
});
