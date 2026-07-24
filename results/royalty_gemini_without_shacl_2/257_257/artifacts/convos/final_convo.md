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
  AssignClass (b835b557-f315-4280-8fbd-21004c585806)
 Call ID: b835b557-f315-4280-8fbd-21004c585806
  Args:
    source: Alexander_Albert_Mountbatten
    type: :Man
  AssignClass (4e3dc40a-41ea-4e0f-9202-994fac1f6dc4)
 Call ID: 4e3dc40a-41ea-4e0f-9202-994fac1f6dc4
  Args:
    source: Alexander_Albert_Mountbatten
    type: :Person
  AddLiteral (c5be67bb-3515-4e09-b722-0d117ddc48e3)
 Call ID: c5be67bb-3515-4e09-b722-0d117ddc48e3
  Args:
    relation: :hasBirthYear
    literal_value: 1886
    literal_type: xsd:integer
    source: Alexander_Albert_Mountbatten
  AddLiteral (42079f12-049d-4a55-abcc-086751574934)
 Call ID: 42079f12-049d-4a55-abcc-086751574934
  Args:
    relation: :hasDeathYear
    literal_value: 1960
    literal_type: xsd:integer
    source: Alexander_Albert_Mountbatten
  AddLiteral (86c4c41e-6f5c-45c0-95dc-1bcae47f6b06)
 Call ID: 86c4c41e-6f5c-45c0-95dc-1bcae47f6b06
  Args:
    source: Alexander_Albert_Mountbatten
    literal_type: xsd:string
    literal_value: Drino
    relation: :knownAs
  AssignClass (7bb9f2d8-abc8-4f27-a331-6f3d58ef85fc)
 Call ID: 7bb9f2d8-abc8-4f27-a331-6f3d58ef85fc
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (b073387f-14df-4ad2-a0d9-9a807fef4c2a)
 Call ID: b073387f-14df-4ad2-a0d9-9a807fef4c2a
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Person
  AddTriple (b843866b-6362-4fe6-9e44-7d3b2413147f)
 Call ID: b843866b-6362-4fe6-9e44-7d3b2413147f
  Args:
    source: Alexander_Albert_Mountbatten
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
  AssignClass (d1d193c0-39b8-4e28-b417-8f5f2d06c5ce)
 Call ID: d1d193c0-39b8-4e28-b417-8f5f2d06c5ce
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (b213c483-ef06-436a-9e62-db83fc08dcac)
 Call ID: b213c483-ef06-436a-9e62-db83fc08dcac
  Args:
    type: :Person
    source: Princess_Beatrice_of_the_United_Kingdom
  AddTriple (76046736-80a0-47f9-a3bb-127a400dd113)
 Call ID: 76046736-80a0-47f9-a3bb-127a400dd113
  Args:
    relation: :hasMother
    target: Princess_Beatrice_of_the_United_Kingdom
    source: Alexander_Albert_Mountbatten
  AssignClass (b77944cc-b465-42da-bf15-471f72c7f682)
 Call ID: b77944cc-b465-42da-bf15-471f72c7f682
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (77178e4b-c927-4b0f-8cf3-562b867098fb)
 Call ID: 77178e4b-c927-4b0f-8cf3-562b867098fb
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (13f12dbc-f748-45bc-8670-fcb181cdc563)
 Call ID: 13f12dbc-f748-45bc-8670-fcb181cdc563
  Args:
    relation: :hasFather
    target: Prince_Alexander_of_Hesse_and_by_Rhine
    source: Prince_Henry_of_Battenberg
  AssignClass (7f1200db-8a8d-44bc-8059-a1a28bcfd098)
 Call ID: 7f1200db-8a8d-44bc-8059-a1a28bcfd098
  Args:
    type: :Woman
    source: Julia_von_Hauke
  AssignClass (184543b0-c746-4809-b7e7-9d9cd8476e07)
 Call ID: 184543b0-c746-4809-b7e7-9d9cd8476e07
  Args:
    type: :Person
    source: Julia_von_Hauke
  AddTriple (afc62769-f9fa-4641-808b-795595fc1d04)
 Call ID: afc62769-f9fa-4641-808b-795595fc1d04
  Args:
    relation: :hasMother
    target: Julia_von_Hauke
    source: Prince_Henry_of_Battenberg
  AssignClass (96b48ac6-9e98-4357-86ef-5cd79e04f7e6)
 Call ID: 96b48ac6-9e98-4357-86ef-5cd79e04f7e6
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (73f2f67d-8c92-4c14-9f83-48ba037316cf)
 Call ID: 73f2f67d-8c92-4c14-9f83-48ba037316cf
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (cb9897c2-d69d-417c-a3bd-e37215504223)
 Call ID: cb9897c2-d69d-417c-a3bd-e37215504223
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (7b8c63ed-ca9a-4958-9d5b-924dc2bfea65)
 Call ID: 7b8c63ed-ca9a-4958-9d5b-924dc2bfea65
  Args:
    source: Prince_Albert
    type: :Person
  AddTriple (60c4580b-82b0-4225-a657-2172c2d6073f)
 Call ID: 60c4580b-82b0-4225-a657-2172c2d6073f
  Args:
    target: Queen_Victoria
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasMother
  AddTriple (a359e3e5-0487-4e5e-a86e-19ccc7d5a874)
 Call ID: a359e3e5-0487-4e5e-a86e-19ccc7d5a874
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    target: Prince_Albert
    relation: :hasFather
  AssignClass (8f9c716f-e7b2-46c1-bf76-479077c9c501)
 Call ID: 8f9c716f-e7b2-46c1-bf76-479077c9c501
  Args:
    source: Princess_Victoria_Eugenia
    type: :Woman
  AssignClass (14e9bcad-1e9b-453d-a9ef-aae4e7d128b8)
 Call ID: 14e9bcad-1e9b-453d-a9ef-aae4e7d128b8
  Args:
    source: Princess_Victoria_Eugenia
    type: :Person
  AddTriple (e16c4793-2da0-45ea-b7f2-f5623a0734fe)
 Call ID: e16c4793-2da0-45ea-b7f2-f5623a0734fe
  Args:
    relation: :hasSister
    source: Alexander_Albert_Mountbatten
    target: Princess_Victoria_Eugenia
  AssignClass (96f54009-ff43-4de1-ac8d-dfabec1ec550)
 Call ID: 96f54009-ff43-4de1-ac8d-dfabec1ec550
  Args:
    source: Lady_Irene_Denison
    type: :Woman
  AssignClass (617b1e23-fb36-4b09-914e-7c6bd4db473e)
 Call ID: 617b1e23-fb36-4b09-914e-7c6bd4db473e
  Args:
    type: :Person
    source: Lady_Irene_Denison
  AddLiteral (be54a01b-623d-4dea-8fa1-badecec0d18b)
 Call ID: be54a01b-623d-4dea-8fa1-badecec0d18b
  Args:
    literal_type: xsd:integer
    source: Alexander_Albert_Mountbatten
    literal_value: 1917
    relation: :hasMarriageYear
  AddTriple (fbd78136-a4e5-4f27-9bb0-e3797f2da655)
 Call ID: fbd78136-a4e5-4f27-9bb0-e3797f2da655
  Args:
    source: Alexander_Albert_Mountbatten
    target: Lady_Irene_Denison
    relation: :hasRelation
  AssignClass (67e1fb65-573b-4edb-959b-8fbf7bb7443b)
 Call ID: 67e1fb65-573b-4edb-959b-8fbf7bb7443b
  Args:
    source: 2nd_Earl_of_Londesborough
    type: :Man
  AssignClass (d89c8207-462e-4256-831b-04b821e18d6e)
 Call ID: d89c8207-462e-4256-831b-04b821e18d6e
  Args:
    source: 2nd_Earl_of_Londesborough
    type: :Person
  AssignClass (0add6ad5-d18d-4bb0-a31d-51105fd7f8c0)
 Call ID: 0add6ad5-d18d-4bb0-a31d-51105fd7f8c0
  Args:
    type: :Woman
    source: Lady_Grace_Adelaide_Fane
  AssignClass (27109f27-8327-4817-9c03-c273b757d16f)
 Call ID: 27109f27-8327-4817-9c03-c273b757d16f
  Args:
    type: :Person
    source: Lady_Grace_Adelaide_Fane
  AddTriple (7972e213-e5de-4310-aed3-348162ec7a76)
 Call ID: 7972e213-e5de-4310-aed3-348162ec7a76
  Args:
    relation: :hasFather
    source: Lady_Irene_Denison
    target: 2nd_Earl_of_Londesborough
  AddTriple (c6788b47-a659-42aa-a667-1fe8816eb586)
 Call ID: c6788b47-a659-42aa-a667-1fe8816eb586
  Args:
    target: Lady_Grace_Adelaide_Fane
    source: Lady_Irene_Denison
    relation: :hasMother
  Finish (036392a7-9735-4420-8796-a5d6c628b7ec)
 Call ID: 036392a7-9735-4420-8796-a5d6c628b7ec
  Args: