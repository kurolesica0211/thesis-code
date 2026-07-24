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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (9841ccec-1576-4ef9-9141-dd03a81dd3e7)
 Call ID: 9841ccec-1576-4ef9-9141-dd03a81dd3e7
  Args:
    type: :Man
    source: Luís_of_Orléans-Braganza
  AssignClass (76ce7537-2083-4194-9138-3b07915f9215)
 Call ID: 76ce7537-2083-4194-9138-3b07915f9215
  Args:
    type: :Person
    source: Luís_of_Orléans-Braganza
  AddLiteral (833f50f3-2ed1-4b3b-abfd-a8879ef604ca)
 Call ID: 833f50f3-2ed1-4b3b-abfd-a8879ef604ca
  Args:
    literal_value: 1878
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Luís_of_Orléans-Braganza
  AddLiteral (de861673-9524-4eeb-a454-aaebf5fdcb98)
 Call ID: de861673-9524-4eeb-a454-aaebf5fdcb98
  Args:
    literal_type: xsd:integer
    literal_value: 1920
    source: Luís_of_Orléans-Braganza
    relation: :hasDeathYear
  AddLiteral (a5e40d1d-ab2d-4b0d-ae76-cddf74f9c00f)
 Call ID: a5e40d1d-ab2d-4b0d-ae76-cddf74f9c00f
  Args:
    literal_value: the Perfect Prince
    literal_type: xsd:string
    source: Luís_of_Orléans-Braganza
    relation: :knownAs
  AssignClass (ff7fda17-d464-4c36-a5de-653d0ce4d6cd)
 Call ID: ff7fda17-d464-4c36-a5de-653d0ce4d6cd
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (c73f760b-bf46-4063-9ca0-fe4d137260f8)
 Call ID: c73f760b-bf46-4063-9ca0-fe4d137260f8
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (d392fbd7-0741-4a62-bc89-ac71ea8347d5)
 Call ID: d392fbd7-0741-4a62-bc89-ac71ea8347d5
  Args:
    type: :Man
    source: Gaston_Count_of_Eu
  AssignClass (a4f6e60a-c953-4f88-8bb8-d77aac3574f7)
 Call ID: a4f6e60a-c953-4f88-8bb8-d77aac3574f7
  Args:
    type: :Person
    source: Gaston_Count_of_Eu
  AddTriple (c6cd6ed8-d2c6-4247-b784-baa6ce209f8a)
 Call ID: c6cd6ed8-d2c6-4247-b784-baa6ce209f8a
  Args:
    relation: :hasMother
    source: Luís_of_Orléans-Braganza
    target: Isabel_Princess_Imperial_of_Brazil
  AddTriple (35ae7b6a-26bd-4724-9a2c-49689c36cc0c)
 Call ID: 35ae7b6a-26bd-4724-9a2c-49689c36cc0c
  Args:
    relation: :hasFather
    target: Gaston_Count_of_Eu
    source: Luís_of_Orléans-Braganza
  AssignClass (c8b7667c-ec8e-4ab2-83ea-592cabf777db)
 Call ID: c8b7667c-ec8e-4ab2-83ea-592cabf777db
  Args:
    type: :Man
    source: Pedro_of_Orléans-Braganza
  AssignClass (31167fa1-a4d5-4ba9-a2ac-d48ff517d1d7)
 Call ID: 31167fa1-a4d5-4ba9-a2ac-d48ff517d1d7
  Args:
    type: :Person
    source: Pedro_of_Orléans-Braganza
  AddTriple (9fa22734-0623-4012-b1df-6c61e5a60678)
 Call ID: 9fa22734-0623-4012-b1df-6c61e5a60678
  Args:
    relation: :isBrotherOf
    target: Luís_of_Orléans-Braganza
    source: Pedro_of_Orléans-Braganza
  AssignClass (b4d12c78-6726-48c5-be78-0267b335f835)
 Call ID: b4d12c78-6726-48c5-be78-0267b335f835
  Args:
    type: :Man
    source: Antônio_of_Orléans-Braganza
  AssignClass (b43215b2-c6ae-47e0-881b-0e42d2dd1f3a)
 Call ID: b43215b2-c6ae-47e0-881b-0e42d2dd1f3a
  Args:
    type: :Person
    source: Antônio_of_Orléans-Braganza
  AddTriple (7aaa2e57-b467-4428-89ac-e9fe919b5d91)
 Call ID: 7aaa2e57-b467-4428-89ac-e9fe919b5d91
  Args:
    source: Antônio_of_Orléans-Braganza
    target: Luís_of_Orléans-Braganza
    relation: :isBrotherOf
  AssignClass (a6ad9297-06cc-4f41-a204-a5306807b0a7)
 Call ID: a6ad9297-06cc-4f41-a204-a5306807b0a7
  Args:
    type: :Woman
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (ebead4c5-d75a-44eb-82d4-eb08c3d74df8)
 Call ID: ebead4c5-d75a-44eb-82d4-eb08c3d74df8
  Args:
    type: :Person
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AddLiteral (f36052bb-91d7-4e4e-a5bf-bc4cd7680877)
 Call ID: f36052bb-91d7-4e4e-a5bf-bc4cd7680877
  Args:
    source: Luís_of_Orléans-Braganza
    relation: :hasMarriageYear
    literal_value: 1908
    literal_type: xsd:integer
  AddTriple (a72ed66c-087f-47bc-a58a-42e6816a3a83)
 Call ID: a72ed66c-087f-47bc-a58a-42e6816a3a83
  Args:
    relation: :hasRelation
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Luís_of_Orléans-Braganza
  AssignClass (326c2714-ca6f-411e-9c6d-d7d9c3808796)
 Call ID: 326c2714-ca6f-411e-9c6d-d7d9c3808796
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (6227a34a-4556-40f7-8b90-3efa0a08f822)
 Call ID: 6227a34a-4556-40f7-8b90-3efa0a08f822
  Args:
    type: :Person
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (1403ecaa-3799-480a-a14e-4d3ab86ae176)
 Call ID: 1403ecaa-3799-480a-a14e-4d3ab86ae176
  Args:
    source: Luís_of_Orléans-Braganza
    target: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasSon
  AddTriple (fec4e051-9d5a-4fee-b0e2-72005b2a2e1e)
 Call ID: fec4e051-9d5a-4fee-b0e2-72005b2a2e1e
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasMother
  AssignClass (91d045bd-1847-44ce-9e12-a5c06e9b5911)
 Call ID: 91d045bd-1847-44ce-9e12-a5c06e9b5911
  Args:
    type: :Man
    source: Luís_Gastão_of_Orléans-Braganza
  AssignClass (4c12e928-fb00-48f8-994f-50579ae3097a)
 Call ID: 4c12e928-fb00-48f8-994f-50579ae3097a
  Args:
    type: :Person
    source: Luís_Gastão_of_Orléans-Braganza
  AddTriple (2f8b57b6-c184-4c31-8a18-47cce5d4b92f)
 Call ID: 2f8b57b6-c184-4c31-8a18-47cce5d4b92f
  Args:
    target: Luís_Gastão_of_Orléans-Braganza
    source: Luís_of_Orléans-Braganza
    relation: :hasSon
  AddTriple (dd691816-156c-4d94-91f2-e3e07966ea78)
 Call ID: dd691816-156c-4d94-91f2-e3e07966ea78
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Luís_Gastão_of_Orléans-Braganza
    relation: :hasMother
  AssignClass (cbf5dc83-2416-40da-8c91-2a0f444fd7b9)
 Call ID: cbf5dc83-2416-40da-8c91-2a0f444fd7b9
  Args:
    type: :Woman
    source: Pia_Maria_of_Orléans-Braganza
  AssignClass (9387d1ca-058d-43ae-96fa-f68800aec2d9)
 Call ID: 9387d1ca-058d-43ae-96fa-f68800aec2d9
  Args:
    type: :Person
    source: Pia_Maria_of_Orléans-Braganza
  AddTriple (ef11707b-f39d-48dd-8d04-a414c726a4bf)
 Call ID: ef11707b-f39d-48dd-8d04-a414c726a4bf
  Args:
    relation: :hasDaughter
    target: Pia_Maria_of_Orléans-Braganza
    source: Luís_of_Orléans-Braganza
  AddTriple (468ac738-4254-4b7f-ad7f-41c3a2abbcfe)
 Call ID: 468ac738-4254-4b7f-ad7f-41c3a2abbcfe
  Args:
    relation: :hasMother
    source: Pia_Maria_of_Orléans-Braganza
    target: Maria_Pia_of_Bourbon-Two_Sicilies
  Finish (ec6a8e5f-208c-41fa-856f-7539439606b5)
 Call ID: ec6a8e5f-208c-41fa-856f-7539439606b5
  Args: