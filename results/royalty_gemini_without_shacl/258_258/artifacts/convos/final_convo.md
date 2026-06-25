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
Prince Luís of Orléans-Braganza (26 January 1878 – 26 March 1920), nicknamed "the Perfect Prince", was the second son of Isabel, Princess Imperial of Brazil and Prince Gaston, Count of Eu, and patriarch of the Vassouras branch of the House of Orléans-Braganza.
In 1908, the year he married, his older brother Pedro renounced his claim to succeed his mother in her claim to the imperial throne, leaving Dom Luís as her heir.
Childhood

Luís was born at Petrópolis on 26 January 1878, to Prince Gaston d'Orléans, Count of Eu, and Isabel, Princess Imperial of Brazil.
His name in full was Luís Maria Filipe Pedro de Alcântara Gastão Miguel Rafael Gonzaga.
While on a trip to Europe with his family, an earthquake occurred on 23 February 1887, and while his older brother Pedro appeared very nervous and cried, Luís simply stood calm and showed no emotions.
Although Pedro was gentle and likeable, he did not like to study and was often clumsy, while Luís had a strong will, was active and apparently intelligent.
Gaston affirmed in another letter, written in March 1890, that "Baby Pedro  always notable for laziness and ineptness," while "Luís does the identical course work all by himself with admirable distinction and capacity."
Luís was always impelled to action thanks to his restless spirit that would take him in his childhood to sports and as an adult to politics.
When the coup that replaced the monarchy with the republic occurred on 15 November 1889, Isabel preferred to send her children to Petrópolis, where later Luís would remember that "locked up in the palace, they had left us during two long days in the most complete ignorance of what was happening out there" until they were sent back to their parents and then left for forced exile.
In 1890, fifteen-year-old Pedro, thirteen-year-old Luís, and their younger brother Antônio (nicknamed "Totó"), moved along with their parents to the outskirts of Versailles.
Luís's older brother, Pedro, reached the age of majority in 1893, but he had no capacity or desire to assume the monarchist cause.
Luís and his brother Antônio followed their older brother at the same military school.
Meanwhile, Luís was ambitious and active, eager to make his mark on the world.
Luís was seen by his parents as the only member of the Imperial family capable of helping the monarchist movement in Brazil.
However, Luís was prevented from disembarking and was not allowed to set foot on his native land by the republican government.
Luís became engaged to his cousin Maria Pia of Bourbon-Two Sicilies, a granddaughter of a brother of Luís's maternal grandmother, Teresa Cristina.
I Prince Pedro de Alcântara Luís Filipe Maria Gastão Miguel Gabriel Rafael Gonzaga of Orléans and Braganza, having maturely reflected, have resolved to renounce the right that, by the Constitution of the Empire of Brazil, promulgated on March 25, 1824, accords to me the Crown of that nation.
Cannes October 30, 1908 signed: Pedro de Alcântara of Orléans-Braganza


This renunciation was followed by a letter from Isabel to royalists in Brazil:

November 9, 1908,  Eu

Most Excellent Gentlemen Members of the Monarchist Directory,

With all my heart I thank you for the congratulations upon the marriages of my dear children Pedro and Luís.
Luís' took place in Cannes on day 4 with the brilliance that is desired for so solemn an act in the life of my successor to the Throne of Brazil.
Before the marriage of Luís he signed his resignation to the crown of Brazil, and here I send it to you, while keeping here an identical copy.
Luís will engage actively in everything with respect to the monarchy and any good for our land.
I give you all my friendship and confidence,

The marriage of Luís and Maria Pia was celebrated on 4 November at Cannes, and that of Pedro and Elizabeth ten days later at Versailles.
From the union of Luís and Maria Pia three children were born: Pedro Henrique, who became the direct successor to Princess Isabel and Head of the Imperial House of Brazil after her death in 1921; Luís Gastão, and Pia Maria.
Isabel did not take long to reveal her opinion about her grandchildren and wrote in a letter in 1914: "I am sending enclosed a photograph of myself with my grandchildren by Luís.
"


Political activity

With the renunciation of the throne by his brother, Luís could finally collaborate effectively with the Brazilian monarchic movement, assuming clearly his position as heir to the throne (after his mother) and trying to assume the leadership of the restoration campaign.
Luís defended ideas that were well ahead of his time and the necessity to guarantee worthy conditions of subsistence for the Brazilian workers would only be observed thirty years later during the dictatorship of Getúlio Vargas.
The progressive vision of Luís made him a target for accusations of being a "socialist" and a "radical" when, in reality, his intent was to hinder the work force from adhering to socialism, communism, or even anarchism.
The start of World War I in August 1914 and the invasion of France by Germany made it possible for Luís to once more prove his idealism and activism as, in his own words, he was a "soldier heart and soul".
Luís joined the army while Antônio served as an air force pilot.
While fighting in the trenches of Flanders in 1915 Luís contracted an aggressive type of bone rheumatism that left him very weak and incapable of walking.
As a consequence of his actions in the conflict and for his bravery, Luís received several decorations: Military medal of the Yser, from King Albert I of Belgium; Legion of Honour, in the degree of knight, and the Cross of War from the French government; the British War Medal, the Victory Medal and Star from the Great Britain.
As his mother lived until 1921, her successor in pretense to the throne of Brazil was her grandson, Pedro Henrique, Luís's son.
"He died, unexpectedly, in Cannes, D. Luiz de Orléans e Bragança, died in exile where he was purging the crime of being Pedro II grandson.
Their presence would shame our phrygian cap..."

— Revista do Brasil

Legacy

Prince Luís is largely unknown to Brazilians today.
The authors dedicated the work to His Imperial Highness the Sire Dom Luiz de Orléans-Braganza.
The Municipality of Pimenta Bueno, in the State of Rondônia (Brazil), honored Dom Luís and the entire Brazilian imperial family in 2010 by renaming one of its streets "Príncipe Dom Luiz de Órleans e Bragança".



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e375131c-f89d-4c57-b29b-a1bddf6ff86a)
 Call ID: e375131c-f89d-4c57-b29b-a1bddf6ff86a
  Args:
    source: :Luis_de_Orleans-Braganza
    type: :Man
  AssignClass (fb36bb46-bdc7-4d7d-a73b-d93e86a25caa)
 Call ID: fb36bb46-bdc7-4d7d-a73b-d93e86a25caa
  Args:
    type: :Person
    source: :Luis_de_Orleans-Braganza
  AddLiteral (37bae3dd-1847-444a-adf7-12b1ff862201)
 Call ID: 37bae3dd-1847-444a-adf7-12b1ff862201
  Args:
    literal_value: 1878
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Luis_de_Orleans-Braganza
  AddLiteral (c8c0adee-8dea-45f4-afb9-1bf1c4df2642)
 Call ID: c8c0adee-8dea-45f4-afb9-1bf1c4df2642
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Luis_de_Orleans-Braganza
    literal_value: 1920
  AddLiteral (285cb717-07b0-48af-94f5-52979b777213)
 Call ID: 285cb717-07b0-48af-94f5-52979b777213
  Args:
    source: :Luis_de_Orleans-Braganza
    literal_type: xsd:string
    relation: :knownAs
    literal_value: the Perfect Prince
  AssignClass (24534077-d4f0-4778-8dee-f107e622303f)
 Call ID: 24534077-d4f0-4778-8dee-f107e622303f
  Args:
    source: :Isabel_Princess_Imperial_of_Brazil
    type: :Woman
  AssignClass (83d79503-e15e-4953-9dac-750f3a71b2c1)
 Call ID: 83d79503-e15e-4953-9dac-750f3a71b2c1
  Args:
    source: :Isabel_Princess_Imperial_of_Brazil
    type: :Person
  AssignClass (7ae395f4-da14-47d5-9123-b17708656eba)
 Call ID: 7ae395f4-da14-47d5-9123-b17708656eba
  Args:
    source: :Gaston_Count_of_Eu
    type: :Man
  AssignClass (f16495f6-0bc4-49d7-9111-25853c74b8d5)
 Call ID: f16495f6-0bc4-49d7-9111-25853c74b8d5
  Args:
    source: :Gaston_Count_of_Eu
    type: :Person
  AddTriple (7cbdb106-b919-448d-8d39-84b2bed8f64b)
 Call ID: 7cbdb106-b919-448d-8d39-84b2bed8f64b
  Args:
    relation: :hasFather
    source: :Luis_de_Orleans-Braganza
    target: :Gaston_Count_of_Eu
  AddTriple (4a31073e-48b0-4796-b812-4c54a210210b)
 Call ID: 4a31073e-48b0-4796-b812-4c54a210210b
  Args:
    target: :Isabel_Princess_Imperial_of_Brazil
    source: :Luis_de_Orleans-Braganza
    relation: :hasMother
  AssignClass (1ef90c56-56cd-4095-b2da-0213cf08771a)
 Call ID: 1ef90c56-56cd-4095-b2da-0213cf08771a
  Args:
    source: :Pedro_of_Orleans-Braganza
    type: :Man
  AssignClass (3d022c06-be20-4634-9d9c-8657aefd659d)
 Call ID: 3d022c06-be20-4634-9d9c-8657aefd659d
  Args:
    source: :Pedro_of_Orleans-Braganza
    type: :Person
  AddTriple (19421a2e-42d6-4bef-8ce2-980132d69087)
 Call ID: 19421a2e-42d6-4bef-8ce2-980132d69087
  Args:
    target: :Luis_de_Orleans-Braganza
    relation: :isBrotherOf
    source: :Pedro_of_Orleans-Braganza
  AssignClass (23f0d780-5db0-49f7-87ae-bb234fa86b28)
 Call ID: 23f0d780-5db0-49f7-87ae-bb234fa86b28
  Args:
    source: :Antonio_of_Orleans-Braganza
    type: :Man
  AssignClass (1275aa90-0574-4d84-b3fd-ca76b90d8486)
 Call ID: 1275aa90-0574-4d84-b3fd-ca76b90d8486
  Args:
    type: :Person
    source: :Antonio_of_Orleans-Braganza
  AddTriple (42ba1d07-5a7c-4219-8a57-496327db0e66)
 Call ID: 42ba1d07-5a7c-4219-8a57-496327db0e66
  Args:
    source: :Antonio_of_Orleans-Braganza
    relation: :isBrotherOf
    target: :Luis_de_Orleans-Braganza
  AssignClass (bd0f8450-d97e-42a7-87d6-826b9cfd3279)
 Call ID: bd0f8450-d97e-42a7-87d6-826b9cfd3279
  Args:
    source: :Maria_Pia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (9ba234e8-8044-4eb5-b3fd-b1d4ff3b7cbd)
 Call ID: 9ba234e8-8044-4eb5-b3fd-b1d4ff3b7cbd
  Args:
    source: :Maria_Pia_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (3c7fb8f2-e37d-4c27-be87-e9f6683e8b18)
 Call ID: 3c7fb8f2-e37d-4c27-be87-e9f6683e8b18
  Args:
    source: :Luis_de_Orleans-Braganza
    relation: :hasRelation
    target: :Maria_Pia_of_Bourbon-Two_Sicilies
  AddLiteral (74883c73-3627-492f-a677-e494aac9c51a)
 Call ID: 74883c73-3627-492f-a677-e494aac9c51a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Luis_de_Orleans-Braganza
    literal_value: 1908
  AssignClass (08bf1499-71f9-4c70-b070-1d596ec4f80c)
 Call ID: 08bf1499-71f9-4c70-b070-1d596ec4f80c
  Args:
    type: :Man
    source: :Pedro_Henrique_of_Orleans-Braganza
  AssignClass (00575613-557b-49c4-b0db-bd1b6b131552)
 Call ID: 00575613-557b-49c4-b0db-bd1b6b131552
  Args:
    type: :Person
    source: :Pedro_Henrique_of_Orleans-Braganza
  AddTriple (7e80ace0-fa00-490b-a011-ad8490d324ca)
 Call ID: 7e80ace0-fa00-490b-a011-ad8490d324ca
  Args:
    relation: :hasFather
    source: :Pedro_Henrique_of_Orleans-Braganza
    target: :Luis_de_Orleans-Braganza
  AddTriple (963cdbbb-39ea-4b80-ad50-42c75aff2622)
 Call ID: 963cdbbb-39ea-4b80-ad50-42c75aff2622
  Args:
    target: :Maria_Pia_of_Bourbon-Two_Sicilies
    source: :Pedro_Henrique_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (6cfbfb17-4714-4c83-a6c3-9fd21782109d)
 Call ID: 6cfbfb17-4714-4c83-a6c3-9fd21782109d
  Args:
    source: :Luis_Gastao_of_Orleans-Braganza
    type: :Man
  AssignClass (6f7a75e9-80f9-4cb2-b0b2-dc4b8632b078)
 Call ID: 6f7a75e9-80f9-4cb2-b0b2-dc4b8632b078
  Args:
    type: :Person
    source: :Luis_Gastao_of_Orleans-Braganza
  AddTriple (cd809f3a-34a7-4dec-badb-96cc7bda2a6c)
 Call ID: cd809f3a-34a7-4dec-badb-96cc7bda2a6c
  Args:
    relation: :hasFather
    source: :Luis_Gastao_of_Orleans-Braganza
    target: :Luis_de_Orleans-Braganza
  AddTriple (d9e6cb17-6011-46c2-9279-b13f1951ad4e)
 Call ID: d9e6cb17-6011-46c2-9279-b13f1951ad4e
  Args:
    target: :Maria_Pia_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: :Luis_Gastao_of_Orleans-Braganza
  AssignClass (a113c124-2be9-472c-bbf7-320018e5d5c0)
 Call ID: a113c124-2be9-472c-bbf7-320018e5d5c0
  Args:
    source: :Pia_Maria_of_Orleans-Braganza
    type: :Woman
  AssignClass (cd7d1652-a941-4d42-9963-2d685c3ecf45)
 Call ID: cd7d1652-a941-4d42-9963-2d685c3ecf45
  Args:
    type: :Person
    source: :Pia_Maria_of_Orleans-Braganza
  AddTriple (48413ec8-62e6-4757-be06-33fbe4106451)
 Call ID: 48413ec8-62e6-4757-be06-33fbe4106451
  Args:
    target: :Luis_de_Orleans-Braganza
    source: :Pia_Maria_of_Orleans-Braganza
    relation: :hasFather
  AddTriple (f0768a6a-fbbc-4312-8688-fad4d3b67723)
 Call ID: f0768a6a-fbbc-4312-8688-fad4d3b67723
  Args:
    relation: :hasMother
    source: :Pia_Maria_of_Orleans-Braganza
    target: :Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (b66ca08d-3350-441f-b336-a7dbe9604699)
 Call ID: b66ca08d-3350-441f-b336-a7dbe9604699
  Args:
    source: :Teresa_Cristina_of_the_Two_Sicilies
    type: :Woman
  AssignClass (a4748f31-d1bd-48d3-9c70-1872ffd7fc33)
 Call ID: a4748f31-d1bd-48d3-9c70-1872ffd7fc33
  Args:
    type: :Person
    source: :Teresa_Cristina_of_the_Two_Sicilies
  AddTriple (c9a9a5fd-4ed4-4806-bc2b-ce97dbd91de2)
 Call ID: c9a9a5fd-4ed4-4806-bc2b-ce97dbd91de2
  Args:
    target: :Teresa_Cristina_of_the_Two_Sicilies
    relation: :hasMother
    source: :Isabel_Princess_Imperial_of_Brazil
  Finish (84b45718-781d-4f0c-8fa7-76799501a28a)
 Call ID: 84b45718-781d-4f0c-8fa7-76799501a28a
  Args: