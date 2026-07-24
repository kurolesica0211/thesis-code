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
  AssignClass (24a9e89b-cafc-4439-bfe6-342b23f307a8)
 Call ID: 24a9e89b-cafc-4439-bfe6-342b23f307a8
  Args:
    type: :Man
    source: Alexander_Albert_Mountbatten
  AssignClass (af46532e-e68a-42ee-b734-96e79969b2ee)
 Call ID: af46532e-e68a-42ee-b734-96e79969b2ee
  Args:
    type: :Person
    source: Alexander_Albert_Mountbatten
  AddLiteral (f6a0a3a7-196a-470d-aae3-ea71b891d72d)
 Call ID: f6a0a3a7-196a-470d-aae3-ea71b891d72d
  Args:
    literal_value: 1886
    relation: :hasBirthYear
    source: Alexander_Albert_Mountbatten
    literal_type: xsd:integer
  AddLiteral (26956317-1db9-4789-863b-df6a7a52d040)
 Call ID: 26956317-1db9-4789-863b-df6a7a52d040
  Args:
    relation: :hasDeathYear
    source: Alexander_Albert_Mountbatten
    literal_type: xsd:integer
    literal_value: 1960
  AddLiteral (b61726f2-47cf-495c-a96e-b76cf504823a)
 Call ID: b61726f2-47cf-495c-a96e-b76cf504823a
  Args:
    literal_value: Drino
    source: Alexander_Albert_Mountbatten
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (c370fccb-9ba2-462b-aaad-833e153dd6ef)
 Call ID: c370fccb-9ba2-462b-aaad-833e153dd6ef
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (1a268892-6635-48fc-aa30-4ce742df306f)
 Call ID: 1a268892-6635-48fc-aa30-4ce742df306f
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AddTriple (e4b5f427-c168-4484-a7be-4e7d9efaf839)
 Call ID: e4b5f427-c168-4484-a7be-4e7d9efaf839
  Args:
    source: Alexander_Albert_Mountbatten
    relation: :hasFather
    target: Prince_Henry_of_Battenberg
  AssignClass (b67f89c2-c6eb-49e3-839e-5055998d93ba)
 Call ID: b67f89c2-c6eb-49e3-839e-5055998d93ba
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (8d21add3-d983-4c49-87da-43258f799444)
 Call ID: 8d21add3-d983-4c49-87da-43258f799444
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Person
  AddTriple (97bc66b1-c838-454f-9cd3-d7f90989d867)
 Call ID: 97bc66b1-c838-454f-9cd3-d7f90989d867
  Args:
    source: Alexander_Albert_Mountbatten
    relation: :hasMother
    target: Princess_Beatrice_of_the_United_Kingdom
  AssignClass (70866114-80f2-4c91-a32c-9d3e22ae1f02)
 Call ID: 70866114-80f2-4c91-a32c-9d3e22ae1f02
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (66e58c02-3514-4119-a30d-48242e4a7c8f)
 Call ID: 66e58c02-3514-4119-a30d-48242e4a7c8f
  Args:
    type: :Person
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AddTriple (894c7ce2-2eed-47e8-81ae-5f2a13bb473f)
 Call ID: 894c7ce2-2eed-47e8-81ae-5f2a13bb473f
  Args:
    source: Prince_Henry_of_Battenberg
    relation: :hasFather
    target: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (30c7f6ab-e222-45ad-9c9d-6a507423f78b)
 Call ID: 30c7f6ab-e222-45ad-9c9d-6a507423f78b
  Args:
    type: :Woman
    source: Julia_von_Hauke
  AssignClass (8e422c70-fa05-402c-8c36-67aeaa20e1ef)
 Call ID: 8e422c70-fa05-402c-8c36-67aeaa20e1ef
  Args:
    type: :Person
    source: Julia_von_Hauke
  AddTriple (cf5c83f1-3faf-4d01-9c66-2b7dcf14e1ac)
 Call ID: cf5c83f1-3faf-4d01-9c66-2b7dcf14e1ac
  Args:
    source: Prince_Henry_of_Battenberg
    relation: :hasMother
    target: Julia_von_Hauke
  AssignClass (e8696fe0-4035-447b-b9af-f6ec438e321b)
 Call ID: e8696fe0-4035-447b-b9af-f6ec438e321b
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (a5c8f067-c933-458b-9e11-6cd2ff03f73b)
 Call ID: a5c8f067-c933-458b-9e11-6cd2ff03f73b
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (1ca07b75-6c28-46bf-b8a2-2c67794fc92a)
 Call ID: 1ca07b75-6c28-46bf-b8a2-2c67794fc92a
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (8bf75c5d-91af-4a14-a220-c48e1345e6d8)
 Call ID: 8bf75c5d-91af-4a14-a220-c48e1345e6d8
  Args:
    source: Prince_Albert
    type: :Person
  AddTriple (35211822-0c5c-4b33-a3bd-7ffbcb086972)
 Call ID: 35211822-0c5c-4b33-a3bd-7ffbcb086972
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasMother
    target: Queen_Victoria
  AddTriple (57bdee84-68b6-4eec-8490-0152c0e90a1b)
 Call ID: 57bdee84-68b6-4eec-8490-0152c0e90a1b
  Args:
    target: Prince_Albert
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasFather
  AssignClass (559bbadd-ed6e-40b6-af64-813c88f5b719)
 Call ID: 559bbadd-ed6e-40b6-af64-813c88f5b719
  Args:
    source: Princess_Victoria_Eugenia
    type: :Woman
  AssignClass (4ea177d8-997e-4109-9bc2-783a3bf6fa63)
 Call ID: 4ea177d8-997e-4109-9bc2-783a3bf6fa63
  Args:
    source: Princess_Victoria_Eugenia
    type: :Person
  AddTriple (7a45be7c-74f3-4be6-9d22-110b9d59a9ec)
 Call ID: 7a45be7c-74f3-4be6-9d22-110b9d59a9ec
  Args:
    source: Princess_Victoria_Eugenia
    relation: :isSisterOf
    target: Alexander_Albert_Mountbatten
  AssignClass (ef16b7d9-de9f-490d-9158-ea130fbf37d3)
 Call ID: ef16b7d9-de9f-490d-9158-ea130fbf37d3
  Args:
    type: :Woman
    source: Lady_Irene_Denison
  AssignClass (ae8bcc03-bb2b-40b9-8816-d36ee204e39b)
 Call ID: ae8bcc03-bb2b-40b9-8816-d36ee204e39b
  Args:
    source: Lady_Irene_Denison
    type: :Person
  AddLiteral (c9d30517-ff67-4609-b7c3-9be67b315055)
 Call ID: c9d30517-ff67-4609-b7c3-9be67b315055
  Args:
    literal_value: 1917
    literal_type: xsd:integer
    source: Alexander_Albert_Mountbatten
    relation: :hasMarriageYear
  AddTriple (9737c06b-d1cb-49bc-86c3-eff3d65e8034)
 Call ID: 9737c06b-d1cb-49bc-86c3-eff3d65e8034
  Args:
    target: Lady_Irene_Denison
    source: Alexander_Albert_Mountbatten
    relation: :hasRelation
  AssignClass (e48f9921-0ab4-42b4-840c-5bd19d4f17cf)
 Call ID: e48f9921-0ab4-42b4-840c-5bd19d4f17cf
  Args:
    source: 2nd_Earl_of_Londesborough
    type: :Man
  AssignClass (13853fe9-8c92-4f95-a640-bdfa2df09cf6)
 Call ID: 13853fe9-8c92-4f95-a640-bdfa2df09cf6
  Args:
    source: 2nd_Earl_of_Londesborough
    type: :Person
  AssignClass (66c956f2-181d-4af3-a4eb-3c8125f87bb2)
 Call ID: 66c956f2-181d-4af3-a4eb-3c8125f87bb2
  Args:
    type: :Woman
    source: Lady_Grace_Adelaide_Fane
  AssignClass (86d38fbf-e9a4-412d-a508-9a43a8239240)
 Call ID: 86d38fbf-e9a4-412d-a508-9a43a8239240
  Args:
    type: :Person
    source: Lady_Grace_Adelaide_Fane
  AddTriple (a8218720-c66a-428b-8148-1be1d46f74dd)
 Call ID: a8218720-c66a-428b-8148-1be1d46f74dd
  Args:
    target: 2nd_Earl_of_Londesborough
    source: Lady_Irene_Denison
    relation: :hasFather
  AddTriple (f538d2a5-d9b6-46e6-8c81-adf550db84e2)
 Call ID: f538d2a5-d9b6-46e6-8c81-adf550db84e2
  Args:
    target: Lady_Grace_Adelaide_Fane
    source: Lady_Irene_Denison
    relation: :hasMother
  Finish (5a38ff20-0b5d-4bf2-b5eb-45c8b278a376)
 Call ID: 5a38ff20-0b5d-4bf2-b5eb-45c8b278a376
  Args: