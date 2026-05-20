================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Irene of Greece and Denmark (Greek: Ειρήνη, romanized: Iríni; 11 May 1942 – 15 January 2026) was the youngest child and second daughter of King Paul of Greece and his wife, Queen Frederica.
She was the younger sister of Queen Sofía of Spain and King Constantine II of Greece.
From 1981 until her death, Irene lived permanently in Spain, becoming a part of the wider Spanish royal family as Queen Sofía's sister, to whose family she remained very close.
Early life

Irene was born on 11 May 1942 in Cape Town, Union of South Africa, where her parents were living in exile because of the German invasion of Greece during the Second World War.
She was the younger daughter of Paul, Crown Prince of Greece (later King Paul), and his wife Frederica of Hanover.
She was christened three weeks after her birth at her parents' Claremont rented home by the Metropolitan of the Holy Archdiocese of Johannesburg and Pretoria and was named after her paternal aunt Princess Irene, Duchess of Aosta.
She had ten godparents, including General Jan Smuts, Lady Katherine Brandram (her paternal aunt), King George II of Greece (her paternal uncle), Queen Mary of the United Kingdom, and the Duchess of Kent (her paternal first cousin once removed).
In 1944 the family moved to Egypt and returned to Greece in 1946 after the approval of the continuity of the Greek monarchy in the referendum with her uncle George II.
Irene was educated at Arsakion school at Psykhikó Palace in Greece and at Schule Schloss Salem in Baden-Württemberg, Germany.
Irene took up the piano in 1962.
As a young woman, Irene was courted by Prince Michel, Count of Évreux, younger son of the Orléanist pretender Henri, Count of Paris, until he met and later married a French noblewoman without his father's consent in 1967.
She was also rumoured to be a potential bride of Crown Prince Harald of Norway (later King Harald V) who later married Sonja Haraldsen in 1968.
Irene was one of the bridesmaids at the wedding of Spanish Prince Juan Carlos and Princess Sofía in 1962.
Her brother Constantine became King in 1964 after the death of their father.
Between her father's death and the birth of her niece Princess Alexia, Irene was heiress presumptive to the Greek throne.
Exile and later life

After her brother was dethroned in the Colonels' coup of 21 April 1967, Irene and the Royal Family moved to Italy after Constantine's unsuccessful countercoup against the junta.
With her mother Irene resided in Rome.
As Mahadevan grew frailer, he dictated his memoirs to Irene.
After her mother's death in 1981, she lived in Spain in an apartment at the Palace of Zarzuela in Madrid, the residence of her sister and brother-in-law, Queen Sofía and King Juan Carlos.
In the 1980s, during the BSE outbreak, Irene arranged for thousands of surplus cows from Europe and the United States to be shipped to India where they evaded slaughter.
During the 1981 Spanish coup attempt, Irene was at the Palace of Zarzuela with King Juan Carlos and her sister Queen Sofia; years later, she recounted the fear they both experienced when remembering the coup in Greece years earlier.
Irene accompanied Sofia in her official duties albeit discreetly.
In 2002, the European Court of Human Rights awarded her £500,000 to compensate for the loss of her family's Greek property, and she donated the entire sum to charity.
In 2007, her biography Irene of Greece, the Rebel Princess was published.
On 16 March 2018, Irene obtained Spanish nationality and renounced her Greek nationality.
Personal life

Irene never married and had a passion for piano and archaeology.
With Sofía, they excavated the sites of the ancient village of Decelea and both, together with archaeologist Theophanó A. Arvanitopoulou, wrote two essays.
In 2000, Irene donated a selection of rare books and archaeological artefacts from the family collection to the Benaki Museum.
After the death of her father Paul, Irene became vegetarian.
In November 2023 it was made public that Irene was suffering from cognitive impairment.
Irene's last public appearance was at the wedding of her nephew and godson Prince Nikolaos in February 2025 in Athens.
In the summer of that year, her illness worsened, so she withdrew from public activities in which she accompanied her sister Queen Sofia, who adapted her schedule to Irene's condition.
On 13 January 2026, the Spanish Royal Household announced her condition had worsened and Queen Sofía cancelled all her public engagements to be at her side.
She died at the Palace of Zarzuela in Madrid, Spain, on 15 January, at the age of 83.
After private services at the Palace of Zarzuela, Irene's body—escorted by the Royal Guard—was laid in repose at the Cathedral of St Andrew and St Demetrius in Madrid on 17 January.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (49e3fccc-3017-4467-bb92-1ce26a11ae98)
 Call ID: 49e3fccc-3017-4467-bb92-1ce26a11ae98
  Args:
    type: :Woman
    source: PrincessIreneOfGreeceAndDenmark
  AssignClass (63f7cd93-8179-4fba-b07c-8517623c13bd)
 Call ID: 63f7cd93-8179-4fba-b07c-8517623c13bd
  Args:
    type: :Man
    source: KingPaulOfGreece
  AssignClass (5761ffa9-9f18-49c4-ac18-24edb9c7b1cc)
 Call ID: 5761ffa9-9f18-49c4-ac18-24edb9c7b1cc
  Args:
    type: :Woman
    source: QueenFredericaOfGreece
  AssignClass (d7232ab5-fa7e-4ac9-bbc7-b00748e61b75)
 Call ID: d7232ab5-fa7e-4ac9-bbc7-b00748e61b75
  Args:
    type: :Woman
    source: QueenSofiaOfSpain
  AssignClass (3a8f60ed-5d19-4d27-98cb-829032974cfd)
 Call ID: 3a8f60ed-5d19-4d27-98cb-829032974cfd
  Args:
    type: :Man
    source: KingConstantineIIOfGreece
  AddTriple (80824296-e8a4-4dbe-9b5a-8831a0b8e82a)
 Call ID: 80824296-e8a4-4dbe-9b5a-8831a0b8e82a
  Args:
    target: KingPaulOfGreece
    relation: :hasFather
    source: PrincessIreneOfGreeceAndDenmark
  AddTriple (aff21d0f-0bd4-408b-9bab-2085bc75f78a)
 Call ID: aff21d0f-0bd4-408b-9bab-2085bc75f78a
  Args:
    target: QueenFredericaOfGreece
    relation: :hasMother
    source: PrincessIreneOfGreeceAndDenmark
  AddTriple (a4e59e37-84c4-4857-b358-380e58c27069)
 Call ID: a4e59e37-84c4-4857-b358-380e58c27069
  Args:
    target: QueenSofiaOfSpain
    source: PrincessIreneOfGreeceAndDenmark
    relation: :isSisterOf
  AddTriple (d58563b5-fa9f-434e-881b-3f398623268a)
 Call ID: d58563b5-fa9f-434e-881b-3f398623268a
  Args:
    source: PrincessIreneOfGreeceAndDenmark
    relation: :isSisterOf
    target: KingConstantineIIOfGreece
  AddLiteral (a660e0ce-dfaa-432d-9893-86453a28ca11)
 Call ID: a660e0ce-dfaa-432d-9893-86453a28ca11
  Args:
    source: PrincessIreneOfGreeceAndDenmark
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1942
  AddLiteral (8de566ff-a7b9-4c55-8cdf-5a02d0b73fd3)
 Call ID: 8de566ff-a7b9-4c55-8cdf-5a02d0b73fd3
  Args:
    literal_value: 2026
    relation: :hasDeathYear
    source: PrincessIreneOfGreeceAndDenmark
    literal_type: xsd:integer
  Finish (d303f2c5-1543-4f28-8f7b-57dcfdc73227)
 Call ID: d303f2c5-1543-4f28-8f7b-57dcfdc73227
  Args: