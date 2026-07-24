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
  AssignClass (29b042a4-b993-437e-a47d-38a35540391e)
 Call ID: 29b042a4-b993-437e-a47d-38a35540391e
  Args:
    source: Luís_of_Orléans-Braganza
    type: :Man
  AssignClass (d1df5d15-1b28-49ad-8df2-32f3d2e42a52)
 Call ID: d1df5d15-1b28-49ad-8df2-32f3d2e42a52
  Args:
    source: Luís_of_Orléans-Braganza
    type: :Person
  AddLiteral (14c1630b-85d3-4462-a89a-859e18253847)
 Call ID: 14c1630b-85d3-4462-a89a-859e18253847
  Args:
    literal_value: 1878
    literal_type: xsd:integer
    source: Luís_of_Orléans-Braganza
    relation: :hasBirthYear
  AddLiteral (8c0ff222-c484-4ca4-a753-e0bc27381ae2)
 Call ID: 8c0ff222-c484-4ca4-a753-e0bc27381ae2
  Args:
    relation: :hasDeathYear
    source: Luís_of_Orléans-Braganza
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (f8760a75-378a-46a1-b51e-9a97f6d20c72)
 Call ID: f8760a75-378a-46a1-b51e-9a97f6d20c72
  Args:
    literal_value: The Perfect Prince
    relation: :knownAs
    source: Luís_of_Orléans-Braganza
    literal_type: xsd:string
  AssignClass (fa682886-f9f4-4e36-9d61-a531d9f3dcf5)
 Call ID: fa682886-f9f4-4e36-9d61-a531d9f3dcf5
  Args:
    source: Isabel_Princess_Imperial_of_Brazil
    type: :Woman
  AssignClass (c7517c4b-08d1-47cb-829b-f5f848c75f75)
 Call ID: c7517c4b-08d1-47cb-829b-f5f848c75f75
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (404626df-8684-41fc-907f-d3ced8cc6dc2)
 Call ID: 404626df-8684-41fc-907f-d3ced8cc6dc2
  Args:
    source: Gaston_Count_of_Eu
    type: :Man
  AssignClass (a016702a-ecb1-489e-95dd-6e927c5b01b4)
 Call ID: a016702a-ecb1-489e-95dd-6e927c5b01b4
  Args:
    source: Gaston_Count_of_Eu
    type: :Person
  AddTriple (57b6833c-714b-45de-a1f8-756f64143202)
 Call ID: 57b6833c-714b-45de-a1f8-756f64143202
  Args:
    source: Luís_of_Orléans-Braganza
    relation: :hasMother
    target: Isabel_Princess_Imperial_of_Brazil
  AddTriple (7d77eec2-6eff-4ac5-a8cd-9d52f6ce9e7a)
 Call ID: 7d77eec2-6eff-4ac5-a8cd-9d52f6ce9e7a
  Args:
    relation: :hasFather
    source: Luís_of_Orléans-Braganza
    target: Gaston_Count_of_Eu
  AssignClass (289568ae-64c4-4a6d-8db6-a82d5a296dfb)
 Call ID: 289568ae-64c4-4a6d-8db6-a82d5a296dfb
  Args:
    type: :Man
    source: Pedro_of_Orléans-Braganza
  AssignClass (b3a81209-7d0f-4e45-abac-ac241a291692)
 Call ID: b3a81209-7d0f-4e45-abac-ac241a291692
  Args:
    source: Pedro_of_Orléans-Braganza
    type: :Person
  AddTriple (2870fbe0-7250-4329-83ab-95e8f5812375)
 Call ID: 2870fbe0-7250-4329-83ab-95e8f5812375
  Args:
    source: Luís_of_Orléans-Braganza
    relation: :hasBrother
    target: Pedro_of_Orléans-Braganza
  AssignClass (8957d49a-ae9a-4b41-8859-2bdc66e7428d)
 Call ID: 8957d49a-ae9a-4b41-8859-2bdc66e7428d
  Args:
    type: :Man
    source: Antônio_of_Orléans-Braganza
  AssignClass (5e9e600f-ebc2-4c85-ae7d-284b0c0c15a3)
 Call ID: 5e9e600f-ebc2-4c85-ae7d-284b0c0c15a3
  Args:
    source: Antônio_of_Orléans-Braganza
    type: :Person
  AddTriple (b7882cdb-05d0-42a3-bb37-0a572f653f6d)
 Call ID: b7882cdb-05d0-42a3-bb37-0a572f653f6d
  Args:
    relation: :hasBrother
    source: Luís_of_Orléans-Braganza
    target: Antônio_of_Orléans-Braganza
  AssignClass (da06c103-9c88-42c3-ab8f-9fc47e5ecf02)
 Call ID: da06c103-9c88-42c3-ab8f-9fc47e5ecf02
  Args:
    type: :Woman
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (ae1d2488-5021-4c64-89e9-497c97d2bf2d)
 Call ID: ae1d2488-5021-4c64-89e9-497c97d2bf2d
  Args:
    type: :Person
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AddLiteral (37328ddf-cfa1-43ec-94d6-4873e5cad8c6)
 Call ID: 37328ddf-cfa1-43ec-94d6-4873e5cad8c6
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Luís_of_Orléans-Braganza
    literal_value: 1908
  AddTriple (a14e354f-3314-4851-a54a-b158c7aabd32)
 Call ID: a14e354f-3314-4851-a54a-b158c7aabd32
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    source: Luís_of_Orléans-Braganza
  AssignClass (1f79511a-038f-4595-96b3-773bab824ed7)
 Call ID: 1f79511a-038f-4595-96b3-773bab824ed7
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (09f19246-f291-44d5-b475-7cf086cb5666)
 Call ID: 09f19246-f291-44d5-b475-7cf086cb5666
  Args:
    type: :Person
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (d272fc17-5a86-461f-abca-cfc5dae11b10)
 Call ID: d272fc17-5a86-461f-abca-cfc5dae11b10
  Args:
    source: Luís_Gastão_of_Orléans-Braganza
    type: :Man
  AssignClass (6040c2a7-6480-47b3-a1fb-5c7aa4500fef)
 Call ID: 6040c2a7-6480-47b3-a1fb-5c7aa4500fef
  Args:
    type: :Person
    source: Luís_Gastão_of_Orléans-Braganza
  AssignClass (27cce599-f68a-41c1-aa11-4cee568f6ea4)
 Call ID: 27cce599-f68a-41c1-aa11-4cee568f6ea4
  Args:
    source: Pia_Maria_of_Orléans-Braganza
    type: :Woman
  AssignClass (d64b1800-1955-4f63-96a9-2ca92df10988)
 Call ID: d64b1800-1955-4f63-96a9-2ca92df10988
  Args:
    type: :Person
    source: Pia_Maria_of_Orléans-Braganza
  AddTriple (d9e19448-3c95-4093-ab32-463de468e24f)
 Call ID: d9e19448-3c95-4093-ab32-463de468e24f
  Args:
    relation: :hasFather
    source: Pedro_Henrique_of_Orléans-Braganza
    target: Luís_of_Orléans-Braganza
  AddTriple (453cafa6-519e-4a5e-a305-0549562da55e)
 Call ID: 453cafa6-519e-4a5e-a305-0549562da55e
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasMother
  AddTriple (f7ae6592-2527-43b4-bf11-f586dee1b84a)
 Call ID: f7ae6592-2527-43b4-bf11-f586dee1b84a
  Args:
    target: Luís_of_Orléans-Braganza
    relation: :hasFather
    source: Luís_Gastão_of_Orléans-Braganza
  AddTriple (677bff21-89c2-4311-abbd-21d73eb3cf91)
 Call ID: 677bff21-89c2-4311-abbd-21d73eb3cf91
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Luís_Gastão_of_Orléans-Braganza
    relation: :hasMother
  AddTriple (c19911eb-a72b-48a2-b41e-15af07fe951a)
 Call ID: c19911eb-a72b-48a2-b41e-15af07fe951a
  Args:
    source: Pia_Maria_of_Orléans-Braganza
    relation: :hasFather
    target: Luís_of_Orléans-Braganza
  AddTriple (aff6b8e1-8148-4083-b730-691ff3908d8c)
 Call ID: aff6b8e1-8148-4083-b730-691ff3908d8c
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Pia_Maria_of_Orléans-Braganza
  Finish (eec562f5-76ec-4365-9e39-b2fd1b2e72ef)
 Call ID: eec562f5-76ec-4365-9e39-b2fd1b2e72ef
  Args: