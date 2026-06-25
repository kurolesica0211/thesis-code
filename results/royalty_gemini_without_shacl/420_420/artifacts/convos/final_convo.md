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
Donatus, Prince and Landgrave of Hesse (legally Heinrich Donatus Philipp Umberto Prinz und Landgraf von Hessen; born 17 October 1966) is a German businessman and the head of the House of Brabant and the House of Hesse.
He is the eldest son and successor of German aristocrat Moritz, Landgrave of Hesse, and his former wife, Princess Tatiana of Sayn-Wittgenstein-Berleburg (b. 1940).
Donatus's father became the head of the Hesse-Cassel line on the death of his own father, Landgrave Philipp in 1980.
Having also been the adopted son and heir of his distant cousin, Louis, Prince of Hesse and by Rhine, the latter's death in 1968 as the last male of the Hesse-Darmstadt branch left Moritz head of the entire House of Hesse, to which Donatus succeeded.
Profession

Donatus directs the Hessische Hausstiftung (Foundation of the House of Hesse), a foundation (see below) established to curate and showcase the cultural heritage and history of the House of Hesse, a dynasty which ruled the Electorate of Hesse-Cassel until 1866, the Grand Duchy of Hesse and by Rhine until 1918, and whose male-line antecedents and co-lateral ties include the Protestant leader Philip the Magnanimous, the Swedish king Frederick I, Russia's last tsarina Alexandra Feodorovna, the exiled Spanish queen Victoria Eugenie of Battenberg, and Britain's last viceroy of India, the assassinated Louis, Earl Mountbatten of Burma.
Donatus also manages Prinz von Hessen, a winery specializing in production of varietal vintages on his 45 hectare vineyard.
Marriage and issue

Donatus married the daughter of German industrial heir and Chinese honorary citizen Count Hubertus von Faber-Castell, Countess Floria Franziska Marie-Luisa Erika von Faber-Castell (born 14 October 1974, Düsseldorf), in a civil ceremony in Wiesbaden on 25 April 2003.
Prince Donatus and Floria Franziska are 6th cousins, as both descended from Frederick II, Landgrave of Hesse-Kassel and his first wife Princess Mary of Great Britain.
Held at the Johanneskirche and followed by a grand ball in the Green Salon, state room of the former Friedrichshof palace in Kronberg (now a luxury hotel and golf course owned by the House of Hesse's family foundation) where Donatus's ancestress, the German Empress Frederick, Princess Royal, lived in widowhood, more than 300 guests were present.
Among them were Caroline, Princess of Hanover, Princess Benedikte of Denmark, and Gloria, Princess of Thurn and Taxis.
Representative appearances

In 2021, Donatus was one of only 30 mourners at Prince Philip, the Duke of Edinburgh's, funeral at St George's Chapel, Windsor Castle.
King Charles III appointed Donatus his personal representative to the funeral of his first cousin Maximilian, Margrave of Baden, on 13 January 2023.
Although, as a descendant of Queen Victoria, he is only a distant relative of today's British royals who are more closely related to some other princes of Hesse, descendants of Prince Philip's sister Sophie, there is a close connection to the British royal family through Donatus' adoptive grandparents, Louis, Prince of Hesse and by Rhine, and his wife Margaret Campbell Geddes, who were relatives and close friends of Queen Elizabeth II and Prince Philip, as Philip's sister Cecilie had been married to Louis' elder brother Georg Donatus, Hereditary Grand Duke of Hesse.
The late Queen, Prince Philip and Charles (then Prince of Wales) have visited Wolfsgarten on several occasions.
Ancestry

Foundation of the House of Hesse

Founded in 1928, the Foundation of the House of Hesse is the successor institution of a family trust that had been established in 1830, confiscated by the Kingdom of Prussia in 1866, and re-established after partial restitution in 1878.
The latter is mainly shown at Fasanerie Palace in Eichenzell, Hesse, a former summer palace of the Prince Abbots of Fulda that had been taken over by the Landgraves of Hesse after the secularization and mediatisation of the Prince-bishopric of Fulda in 1803.
The Landgrave and his family live in Wolfsgarten and Panker.



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
  AssignClass (e08e6e08-62cd-45bb-8aa0-950a1e771594)
 Call ID: e08e6e08-62cd-45bb-8aa0-950a1e771594
  Args:
    source: Donatus
    type: :Man
  AssignClass (7e36b261-06ff-4fea-8d87-d9fa6b8ba575)
 Call ID: 7e36b261-06ff-4fea-8d87-d9fa6b8ba575
  Args:
    source: Donatus
    type: :Person
  AddLiteral (6a48f382-a417-46ee-8767-ff41431d5971)
 Call ID: 6a48f382-a417-46ee-8767-ff41431d5971
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    source: Donatus
    relation: :hasBirthYear
  AssignClass (f9ba290d-3311-4322-a00e-822cd33c75ef)
 Call ID: f9ba290d-3311-4322-a00e-822cd33c75ef
  Args:
    source: Moritz
    type: :Man
  AssignClass (2f474e4c-2f42-4727-907c-24fd8e361a84)
 Call ID: 2f474e4c-2f42-4727-907c-24fd8e361a84
  Args:
    source: Moritz
    type: :Person
  AssignClass (77b1ada0-974e-4bac-99c7-2924a805d2e3)
 Call ID: 77b1ada0-974e-4bac-99c7-2924a805d2e3
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (c4b174dc-815c-42aa-b278-a73d2f3defd7)
 Call ID: c4b174dc-815c-42aa-b278-a73d2f3defd7
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddLiteral (c703945a-ab9e-4be8-9201-343e1d595610)
 Call ID: c703945a-ab9e-4be8-9201-343e1d595610
  Args:
    literal_type: xsd:integer
    literal_value: 1940
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    relation: :hasBirthYear
  AddTriple (b9eecbf4-50a6-466c-ad52-f63b5665d94c)
 Call ID: b9eecbf4-50a6-466c-ad52-f63b5665d94c
  Args:
    target: Moritz
    source: Donatus
    relation: :hasFather
  AddTriple (e0e3ba99-1f6d-4b4b-b98f-901ca399f351)
 Call ID: e0e3ba99-1f6d-4b4b-b98f-901ca399f351
  Args:
    relation: :hasMother
    source: Donatus
    target: Tatiana_of_Sayn-Wittgenstein-Berleburg
  AssignClass (05019156-f1c5-48b8-a860-eddc0c505471)
 Call ID: 05019156-f1c5-48b8-a860-eddc0c505471
  Args:
    source: Philipp
    type: :Man
  AssignClass (74981e00-fff8-4aa5-8542-1674a33be2cf)
 Call ID: 74981e00-fff8-4aa5-8542-1674a33be2cf
  Args:
    source: Philipp
    type: :Person
  AddTriple (bd552d5f-fd86-4c12-95d3-0499003afc7b)
 Call ID: bd552d5f-fd86-4c12-95d3-0499003afc7b
  Args:
    relation: :hasFather
    source: Moritz
    target: Philipp
  AddLiteral (35d79ef0-731f-4960-8b48-c245cc5e5fb1)
 Call ID: 35d79ef0-731f-4960-8b48-c245cc5e5fb1
  Args:
    relation: :hasDeathYear
    source: Philipp
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (3a452531-2587-489d-a38e-cba9a7994899)
 Call ID: 3a452531-2587-489d-a38e-cba9a7994899
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (27be23c6-8030-432e-9584-f53ecf173975)
 Call ID: 27be23c6-8030-432e-9584-f53ecf173975
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Person
  AddLiteral (2bf0d129-7812-4a81-a335-25766e6927af)
 Call ID: 2bf0d129-7812-4a81-a335-25766e6927af
  Args:
    literal_type: xsd:integer
    literal_value: 1968
    source: Louis_Prince_of_Hesse_and_by_Rhine
    relation: :hasDeathYear
  AssignClass (bacc4ffd-559c-42b1-aad2-26957e32ee4c)
 Call ID: bacc4ffd-559c-42b1-aad2-26957e32ee4c
  Args:
    source: Floria_Franziska_von_Faber-Castell
    type: :Woman
  AssignClass (64999ed6-9990-481c-b6df-ec5c5d7f3d3d)
 Call ID: 64999ed6-9990-481c-b6df-ec5c5d7f3d3d
  Args:
    source: Floria_Franziska_von_Faber-Castell
    type: :Person
  AddLiteral (1b80e141-626b-4b18-ab76-7045423494ef)
 Call ID: 1b80e141-626b-4b18-ab76-7045423494ef
  Args:
    literal_value: 1974
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Floria_Franziska_von_Faber-Castell
  AddTriple (bb370518-d8d7-4c8b-aa1a-27118e8ad8b2)
 Call ID: bb370518-d8d7-4c8b-aa1a-27118e8ad8b2
  Args:
    relation: :hasRelation
    source: Donatus
    target: Floria_Franziska_von_Faber-Castell
  AddLiteral (5b2b9378-a540-4216-bcee-9ae8d83ad08c)
 Call ID: 5b2b9378-a540-4216-bcee-9ae8d83ad08c
  Args:
    literal_value: 2003
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Donatus
  AssignClass (12f18da5-51f2-47e3-87ec-6455de843a97)
 Call ID: 12f18da5-51f2-47e3-87ec-6455de843a97
  Args:
    source: Hubertus_von_Faber-Castell
    type: :Man
  AssignClass (55c9a94e-2101-4bf6-a28a-19c0a4e37a2a)
 Call ID: 55c9a94e-2101-4bf6-a28a-19c0a4e37a2a
  Args:
    source: Hubertus_von_Faber-Castell
    type: :Person
  AddTriple (2ed78d82-c89b-48e8-bbd5-df642bf665de)
 Call ID: 2ed78d82-c89b-48e8-bbd5-df642bf665de
  Args:
    source: Floria_Franziska_von_Faber-Castell
    relation: :hasFather
    target: Hubertus_von_Faber-Castell
  AssignClass (ad99e3da-05e1-47ab-8eff-0a972573a3d2)
 Call ID: ad99e3da-05e1-47ab-8eff-0a972573a3d2
  Args:
    source: Frederick_II_Landgrave_of_Hesse-Kassel
    type: :Man
  AssignClass (34d94559-ea68-4a21-8462-1466d1ecba45)
 Call ID: 34d94559-ea68-4a21-8462-1466d1ecba45
  Args:
    source: Frederick_II_Landgrave_of_Hesse-Kassel
    type: :Person
  AssignClass (80c56fc3-37b9-4454-8fbf-6ef7a3a455b1)
 Call ID: 80c56fc3-37b9-4454-8fbf-6ef7a3a455b1
  Args:
    source: Princess_Mary_of_Great_Britain
    type: :Woman
  AssignClass (11feaea3-aa4e-42b1-b73a-c39036af02f7)
 Call ID: 11feaea3-aa4e-42b1-b73a-c39036af02f7
  Args:
    source: Princess_Mary_of_Great_Britain
    type: :Person
  AddTriple (08753c7a-eb99-4ca5-b8d7-87d06872a4fe)
 Call ID: 08753c7a-eb99-4ca5-b8d7-87d06872a4fe
  Args:
    relation: :isAncestorOf
    source: Frederick_II_Landgrave_of_Hesse-Kassel
    target: Donatus
  AddTriple (6a6e9263-5c02-438b-a5ff-80368632055f)
 Call ID: 6a6e9263-5c02-438b-a5ff-80368632055f
  Args:
    source: Princess_Mary_of_Great_Britain
    relation: :isAncestorOf
    target: Donatus
  AddTriple (c4f1e798-80f0-4f91-b4b3-ee5f72df784a)
 Call ID: c4f1e798-80f0-4f91-b4b3-ee5f72df784a
  Args:
    target: Floria_Franziska_von_Faber-Castell
    source: Frederick_II_Landgrave_of_Hesse-Kassel
    relation: :isAncestorOf
  AddTriple (4e70879c-d40d-43dc-a117-2a4df39e09a4)
 Call ID: 4e70879c-d40d-43dc-a117-2a4df39e09a4
  Args:
    target: Floria_Franziska_von_Faber-Castell
    source: Princess_Mary_of_Great_Britain
    relation: :isAncestorOf
  AssignClass (e228a005-7138-4bc2-93e3-f5c9923a248c)
 Call ID: e228a005-7138-4bc2-93e3-f5c9923a248c
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AssignClass (56474f4c-472a-451e-be18-ec6b380a6407)
 Call ID: 56474f4c-472a-451e-be18-ec6b380a6407
  Args:
    source: Margaret_Campbell_Geddes
    type: :Person
  AssignClass (040db13b-945a-4267-8d4b-2da61f237dc1)
 Call ID: 040db13b-945a-4267-8d4b-2da61f237dc1
  Args:
    source: Cecilie
    type: :Woman
  AssignClass (a5366aa3-1409-4cc5-b629-244053c221f5)
 Call ID: a5366aa3-1409-4cc5-b629-244053c221f5
  Args:
    source: Cecilie
    type: :Person
  AssignClass (dfbc564d-0891-44cd-be86-247add99f114)
 Call ID: dfbc564d-0891-44cd-be86-247add99f114
  Args:
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    type: :Man
  AssignClass (4e1ecb2f-b521-467f-a8a8-c70d4b366790)
 Call ID: 4e1ecb2f-b521-467f-a8a8-c70d4b366790
  Args:
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    type: :Person
  AddTriple (5319ba47-1f4e-45fd-8d40-3628e53bdf65)
 Call ID: 5319ba47-1f4e-45fd-8d40-3628e53bdf65
  Args:
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :isSiblingOf
    target: Louis_Prince_of_Hesse_and_by_Rhine
  AddTriple (0716cd36-64b9-4894-b9e6-48f389dd13c4)
 Call ID: 0716cd36-64b9-4894-b9e6-48f389dd13c4
  Args:
    relation: :hasFather
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    target: Louis_Prince_of_Hesse_and_by_Rhine
  AddTriple (d88d7eed-e0f3-4840-b52d-280cdf887ea9)
 Call ID: d88d7eed-e0f3-4840-b52d-280cdf887ea9
  Args:
    target: Margaret_Campbell_Geddes
    relation: :hasMother
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
  AddTriple (6db81869-2fb0-45a1-8a28-cfdfa023477f)
 Call ID: 6db81869-2fb0-45a1-8a28-cfdfa023477f
  Args:
    target: Louis_Prince_of_Hesse_and_by_Rhine
    relation: :hasFather
    source: Cecilie
  AddTriple (b57b80b3-1198-4cb6-9ed5-f4a8a9709ecb)
 Call ID: b57b80b3-1198-4cb6-9ed5-f4a8a9709ecb
  Args:
    target: Margaret_Campbell_Geddes
    source: Cecilie
    relation: :hasMother
  Finish (07e2de53-30ad-4b35-92b6-0183ffe61fe7)
 Call ID: 07e2de53-30ad-4b35-92b6-0183ffe61fe7
  Args: