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
Alexander Albert Mountbatten, 1st Marquess of Carisbrooke (born Prince Alexander Albert of Battenberg; 23 November 1886 – 23 February 1960) was a British Royal Navy officer, a member of the Hessian princely Battenberg family and the last surviving grandson of Queen Victoria.
Early life

Alexander, known as Drino, was born in 1886 at Windsor Castle in Berkshire and was educated at Wellington College and at the Britannia Royal Naval College.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julie née Countess of Hauke.
His mother was Princess Beatrice of the United Kingdom, the fifth daughter and the youngest child of Queen Victoria and Prince Albert.
Prince Henry of Battenberg was the product of a morganatic marriage and took his style of Prince of Battenberg from his mother, Julia von Hauke, who was created Princess of Battenberg in her own right.
At his birth, Alexander was styled His Serene Highness Prince Alexander of Battenberg because the child of a morganatic marriage is ineligible for "Grand-Ducal Highness" status.
His godparents were Queen Victoria of the United Kingdom (his maternal grandmother), Prince Alexander of Hesse and by Rhine (his paternal grandfather), the Prince of Wales (his maternal uncle), Prince Alexander of Battenberg (his paternal uncle), and Princess Irene of Hesse and by Rhine (his maternal first cousin and paternal second cousin).
Alexander was the brother-in-law to Alfonso XIII of Spain, who married Alexander's sister, Princess Victoria Eugenia, in 1906.
Military service and honours

Alexander passed a qualifying examination to become service cadet in the Royal Navy in March 1902, and subsequently joined the cadet training ship HMS Britannia at Dartmouth on 8 May 1902.
Several of his Mountbatten cousins were also subsequently members, including his first cousins once removed the Marquess of Milford Haven and Duke of Edinburgh.
He held several other foreign orders and decorations: Grand Cross and Collar of Order of Charles III (Spain), Order of Leopold, with swords (Belgium), Order of Saint Alexander Nevsky (Russia), Order of Naval Merit, fourth class (Spain), Order of the Nile (Egypt), Order of the Crown (Romania), and Croix de Guerre, with palms (France).
During World War II, despite being in his mid-fifties, the Marquess joined the Royal Air Force and was commissioned an acting pilot officer on 6 June 1941.
Marquess of Carisbrooke

Anti-German feeling during World War I led George V to change the name of the Royal House in July 1917 from the House of Saxe-Coburg-Gotha to the House of Windsor.
The Battenberg family relinquished their titles of Prince and Princess of Battenberg and the styles of Highness and Serene Highness.
Under royal warrant, they instead took the surname Mountbatten, an Anglicised form of Battenberg.
As such, Prince Alexander became Sir Alexander Mountbatten.
On 7 November 1917, he was created Marquess of Carisbrooke, Earl of Berkhamsted and Viscount Launceston.
In the 1930s, author E. F. Benson dedicated two of his famous novels, Mapp and Lucia and Lucia's Progress, to the Marquess of Carisbrooke.
Marriage

On 19 July 1917, he married Lady Irene Denison (4 July 1890 – 16 July 1956), the only daughter of the 2nd Earl of Londesborough and his wife, Lady Grace Adelaide Fane, at the Chapel Royal of St James's Palace.
Lord and Lady Carisbrooke had one child, a daughter:
Carisbrooke was likely homosexual or bisexual; according to the published diaries of Cecil Beaton, in his later years, Lord Carisbrooke had a longtime male lover, Simon Fleet.
More is written about Lord Carisbrooke and his wife in the published diaries of James Lees-Milne and Henry "Chips" Channon.


Residences

By 1926 Lord and Lady Carisbrooke had established a London residence at No. 4 Belgrave Place, Belgravia, which continued to be their London home until early 1931.
By 1938 Lord and Lady Carisbrooke lived at Kensington Palace.
Following the death of Lady Carisbrooke in 1956, Lord Carisbrooke was granted the use of a grace-and-favour residence, Apartment 10, Kensington Palace, which remained as his home until his death in 1960.
Later career

Lord Carisbrooke, who received no state allowance, became the first member of the British royal family to work in the commercial sector.
Death

Lord Carisbrooke died on 23 February 1960, aged 73, at Kensington Palace.
His ashes were interred within the Battenberg Chapel at St. Mildred's Church, Whippingham, on the Isle of Wight.
As he had no sons, the title Marquess of Carisbrooke became extinct upon his death.



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
  AssignClass (84a43d4b-0b06-49db-a53e-cab9c5b3b97f)
 Call ID: 84a43d4b-0b06-49db-a53e-cab9c5b3b97f
  Args:
    source: Alexander_Mountbatten
    type: :Man
  AssignClass (42277c71-2e2e-4de6-bf20-8ab655a4aac3)
 Call ID: 42277c71-2e2e-4de6-bf20-8ab655a4aac3
  Args:
    source: Alexander_Mountbatten
    type: :Person
  AddLiteral (7aba0e1a-a59e-475e-8804-82ebe3552b87)
 Call ID: 7aba0e1a-a59e-475e-8804-82ebe3552b87
  Args:
    literal_value: 1886
    source: Alexander_Mountbatten
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2891804a-8155-4027-b37e-0195f06bba9e)
 Call ID: 2891804a-8155-4027-b37e-0195f06bba9e
  Args:
    literal_value: 1960
    source: Alexander_Mountbatten
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (ae8b9b2a-e0b1-491b-9c65-6ef740430bb5)
 Call ID: ae8b9b2a-e0b1-491b-9c65-6ef740430bb5
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Drino
    source: Alexander_Mountbatten
  AssignClass (54da3b6f-89e5-4c59-81db-55a1e96de5fe)
 Call ID: 54da3b6f-89e5-4c59-81db-55a1e96de5fe
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (c56ee636-db79-46c7-857b-e5743f48fc83)
 Call ID: c56ee636-db79-46c7-857b-e5743f48fc83
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AddTriple (82a09a64-84e4-4160-8cb8-af738aac1637)
 Call ID: 82a09a64-84e4-4160-8cb8-af738aac1637
  Args:
    relation: :hasFather
    source: Alexander_Mountbatten
    target: Prince_Henry_of_Battenberg
  AssignClass (ae8b23fa-946f-444b-a057-ea177cc3c094)
 Call ID: ae8b23fa-946f-444b-a057-ea177cc3c094
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (d251b525-217f-43b1-b801-f14d47b3bc05)
 Call ID: d251b525-217f-43b1-b801-f14d47b3bc05
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Person
  AddTriple (608c182f-f4ff-4b09-b7e4-b69c5b3f5343)
 Call ID: 608c182f-f4ff-4b09-b7e4-b69c5b3f5343
  Args:
    relation: :hasMother
    source: Alexander_Mountbatten
    target: Princess_Beatrice_of_the_United_Kingdom
  AssignClass (ff7367c4-93f7-4213-ade0-a41fe3ddd31e)
 Call ID: ff7367c4-93f7-4213-ade0-a41fe3ddd31e
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (c7125465-9734-495b-bda9-f08172abf9a5)
 Call ID: c7125465-9734-495b-bda9-f08172abf9a5
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (e8b8b8c3-3b0c-4b18-8e34-c51db1ba322b)
 Call ID: e8b8b8c3-3b0c-4b18-8e34-c51db1ba322b
  Args:
    target: Prince_Alexander_of_Hesse_and_by_Rhine
    source: Prince_Henry_of_Battenberg
    relation: :hasFather
  AssignClass (35197da8-97e3-45ad-8b02-75479e5aa7a5)
 Call ID: 35197da8-97e3-45ad-8b02-75479e5aa7a5
  Args:
    type: :Woman
    source: Julie_Countess_of_Hauke
  AssignClass (338ea329-d6f3-409e-9224-0ed18d9d4c78)
 Call ID: 338ea329-d6f3-409e-9224-0ed18d9d4c78
  Args:
    type: :Person
    source: Julie_Countess_of_Hauke
  AddTriple (0417adcb-c1cc-4dea-8dac-3f15bfb92acb)
 Call ID: 0417adcb-c1cc-4dea-8dac-3f15bfb92acb
  Args:
    relation: :hasMother
    source: Prince_Henry_of_Battenberg
    target: Julie_Countess_of_Hauke
  AssignClass (f2464751-1391-4420-a6ae-31a96eaa04f3)
 Call ID: f2464751-1391-4420-a6ae-31a96eaa04f3
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (4ae1e5d9-db02-48af-8e89-bc48b2d58f75)
 Call ID: 4ae1e5d9-db02-48af-8e89-bc48b2d58f75
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (a4efe3b9-463f-4fda-8898-8732723dfa7c)
 Call ID: a4efe3b9-463f-4fda-8898-8732723dfa7c
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (e1bca00a-a333-4a48-8637-c63c288dca85)
 Call ID: e1bca00a-a333-4a48-8637-c63c288dca85
  Args:
    type: :Person
    source: Prince_Albert
  AddTriple (6ceef61d-65fd-48d5-a291-32b78fb057d4)
 Call ID: 6ceef61d-65fd-48d5-a291-32b78fb057d4
  Args:
    relation: :hasMother
    source: Princess_Beatrice_of_the_United_Kingdom
    target: Queen_Victoria
  AddTriple (9539d2bc-751a-4faf-bbce-e20df4df07bf)
 Call ID: 9539d2bc-751a-4faf-bbce-e20df4df07bf
  Args:
    target: Prince_Albert
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasFather
  AssignClass (e262bd1b-360e-47bb-950c-4917377d3cf2)
 Call ID: e262bd1b-360e-47bb-950c-4917377d3cf2
  Args:
    source: Lady_Irene_Denison
    type: :Woman
  AssignClass (916c1125-c175-417e-8ddb-a75de1f23390)
 Call ID: 916c1125-c175-417e-8ddb-a75de1f23390
  Args:
    type: :Person
    source: Lady_Irene_Denison
  AddLiteral (f488e03a-6332-4405-afdb-44e4a3266c9c)
 Call ID: f488e03a-6332-4405-afdb-44e4a3266c9c
  Args:
    literal_value: 1917
    source: Alexander_Mountbatten
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (9220347b-de16-4fb5-bdcb-28cafce87773)
 Call ID: 9220347b-de16-4fb5-bdcb-28cafce87773
  Args:
    source: Alexander_Mountbatten
    target: Lady_Irene_Denison
    relation: :hasRelation
  AssignClass (7acc728f-d33a-4d62-bb67-6babd70dcb75)
 Call ID: 7acc728f-d33a-4d62-bb67-6babd70dcb75
  Args:
    source: Earl_of_Londesborough_2nd
    type: :Man
  AssignClass (f04ea7d3-94a6-4cda-a290-c167bdf22e44)
 Call ID: f04ea7d3-94a6-4cda-a290-c167bdf22e44
  Args:
    source: Earl_of_Londesborough_2nd
    type: :Person
  AssignClass (f5005d7d-2419-49f1-9b6f-ae7d5bf5dc8b)
 Call ID: f5005d7d-2419-49f1-9b6f-ae7d5bf5dc8b
  Args:
    type: :Woman
    source: Lady_Grace_Adelaide_Fane
  AssignClass (70ac68d4-7417-407f-81c1-25f5dd643729)
 Call ID: 70ac68d4-7417-407f-81c1-25f5dd643729
  Args:
    type: :Person
    source: Lady_Grace_Adelaide_Fane
  AddTriple (0c2c1596-3776-4e92-aa76-e36f9e91876d)
 Call ID: 0c2c1596-3776-4e92-aa76-e36f9e91876d
  Args:
    source: Lady_Irene_Denison
    target: Earl_of_Londesborough_2nd
    relation: :hasFather
  AddTriple (4eb4699c-cff8-48e9-b0b8-59c9c7e5fe2e)
 Call ID: 4eb4699c-cff8-48e9-b0b8-59c9c7e5fe2e
  Args:
    target: Lady_Grace_Adelaide_Fane
    source: Lady_Irene_Denison
    relation: :hasMother
  AssignClass (7e495f6a-1ef1-4b4f-b87c-9889fcd2611b)
 Call ID: 7e495f6a-1ef1-4b4f-b87c-9889fcd2611b
  Args:
    source: Princess_Victoria_Eugenia
    type: :Woman
  AssignClass (155fee29-ea8c-4bfc-8cd9-4e47b3e0a8ba)
 Call ID: 155fee29-ea8c-4bfc-8cd9-4e47b3e0a8ba
  Args:
    source: Princess_Victoria_Eugenia
    type: :Person
  AddTriple (970be60a-ad08-44c5-af05-c0f83e8dbbfc)
 Call ID: 970be60a-ad08-44c5-af05-c0f83e8dbbfc
  Args:
    source: Alexander_Mountbatten
    target: Princess_Victoria_Eugenia
    relation: :hasSister
  AssignClass (4b517c24-1dd0-4874-a66d-4a470d32942f)
 Call ID: 4b517c24-1dd0-4874-a66d-4a470d32942f
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (916af9f1-58ce-4915-92e6-1e1d890ce95c)
 Call ID: 916af9f1-58ce-4915-92e6-1e1d890ce95c
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (1903a4f0-4abb-4fef-bf76-0f217634936b)
 Call ID: 1903a4f0-4abb-4fef-bf76-0f217634936b
  Args:
    relation: :hasRelation
    target: Alfonso_XIII_of_Spain
    source: Princess_Victoria_Eugenia
  Finish (a57547e0-04e3-43e2-86b0-299edbacc6fe)
 Call ID: a57547e0-04e3-43e2-86b0-299edbacc6fe
  Args: