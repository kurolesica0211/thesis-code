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
George Henry Hubert Lascelles, 7th Earl of Harewood (7 February 1923 – 11 July 2011), styled The Honourable George Lascelles before 1929 and Viscount Lascelles between 1929 and 1947, was a British classical music administrator and author, and a member of the extended British royal family, as a maternal grandson of King George V and Queen Mary, and thus a first cousin of Queen Elizabeth II.
Harewood was the elder son of the 6th Earl of Harewood and Princess Mary, Princess Royal, the only daughter of King George V and Queen Mary.
Lord Harewood was the eldest grandchild of King George V and Queen Mary, nephew of both King Edward VIII and King George VI and first cousin of Queen Elizabeth II.
He was the first member of the Royal Family to obtain a divorce (as opposed to an annulment).
he was the director of the Edinburgh Festival from 1961-1965


Early life

George Henry Hubert Lascelles was born at his parents' London home of Chesterfield House on 7 February 1923, the first child of Henry, Viscount Lascelles, and Princess Mary, Viscountess Lascelles, and first grandchild of King George V and Queen Mary, who stood as sponsors at his christening.
The christening took place on 25 March 1923 at St Mary's Church in the village of Goldsborough, near Knaresborough adjoining the family home Goldsborough Hall.
After his paternal grandfather's death in 1929, he was styled as Viscount Lascelles as his father succeeded to the earldom.
He served as a Page of Honour at the coronation of his uncle King George VI in May 1937.
He was raised at Harewood House in Yorkshire.
Military service

Lascelles joined the British Army where he was commissioned as a second lieutenant into the Grenadier Guards (his father's regiment) in 1942, attaining the rank of captain.
As the nephew of King George VI, Lascelles was one of the Prominente at Colditz, considered a potential bargaining chip by the Nazis.
— Lord Harewood, Desert Island Discs, 1982
In March 1945, Adolf Hitler signed his death warrant; the SS general in command of prisoner-of-war camps, Gottlob Berger, realizing the war was lost, refused to carry out the sentence and released Lascelles to the Swiss.
Lord Harewood served as a Counsellor of State in 1947, 1953–54, and 1956.
House of Lords

Lascelles succeeded his father in 1947.
Career

Opera

A music enthusiast, Lord Harewood devoted most of his career to opera with his Yorkshire heritage fostering his interest; in March 1949, as a young single man, he had been among the audience at the Leeds Town Hall for a  performance of operatic works by the Yorkshire Symphony Orchestra.
He was director of the Royal Opera House, Covent Garden from 1951 to 1953 and again from 1969 to 1972.
Lord Harewood served as a governor of the BBC from 1985 to 1987 and as the president of the British Board of Film Classification from 1985 to 1996.
Public life

Lascelles was the only person to serve as Counsellor of State without being a Prince of the United Kingdom, serving from 1945 to 1951, then from 1952 to 1956.
The estate and house, Harewood House, are held by a charity with £9 million of assets, and were not counted as part of his wealth.
In 1959, Harewood received the Grand Decoration in Silver with Sash for Services to the Republic of Austria.
Personal life

Marriages and children

On 29 September 1949 at St. Mark's Church, London, Lord Harewood married Marion Stein, a concert pianist and the daughter of the Viennese music publisher Erwin Stein.
Because of Harewood's position in the line of succession, the marriage was subject to approval from the sovereign, under the Royal Marriages Act 1772.
Queen Mary, mother of George VI, objected to the marriage but permission was eventually granted.
Benjamin Britten, a friend of the Stein family, composed an anthem, "Amo Ergo Sum", for the wedding ceremony.
Lord and Lady Harewood had three sons:


The earl's marriage to Marion Stein ended in divorce in 1967, after the earl's mistress, Patricia "Bambi" Tuckwell – an Australian violinist and sister of the musician Barry Tuckwell – gave birth to his son.
Stein went on to marry politician Jeremy Thorpe.
Lord Harewood married Tuckwell (24 November 1926 – 4 May 2018) on 31 July 1967.
They were obliged to be married abroad as, in England, registry office marriages were barred at the time for persons covered by the Royal Marriages Act, and divorcees could not marry in the Church of England.
They had one son: Mark Lascelles.
Death

Lord Harewood died peacefully at home, on 11 July 2011, aged 88 years.
Arms

Books

The Tongs and the Bones: The Memoirs of Lord Harewood, published by George Weidenfeld & Nicolson (1981), .mw-parser-output cite.citation{font-style:inherit;word-wrap:break-word}.mw-parser-output .citation q{quotes:"\"""\"""'""'"}.mw-parser-output .citation:target{background-color:rgba(0,127,255,0.133)}.mw-parser-output .id-lock-free.id-lock-free a{background:url("//upload.wikimedia.org/wikipedia/commons/6/65/Lock-green.svg")right 0.1em center/9px no-repeat}.mw-parser-output .id-lock-limited.id-lock-limited a,.mw-parser-output .id-lock-registration.id-lock-registration a{background:url("//upload.wikimedia.org/wikipedia/commons/d/d6/Lock-gray-alt-2.svg")right 0.1em center/9px no-repeat}.mw-parser-output .id-lock-subscription.id-lock-subscription a{background:url("//upload.wikimedia.org/wikipedia/commons/a/aa/Lock-red-alt-2.svg")right 0.1em center/9px no-repeat}.mw-parser-output .cs1-ws-icon a{background:url("//upload.wikimedia.org/wikipedia/commons/4/4c/Wikisource-logo.svg")right 0.1em center/12px no-repeat}body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-free a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-limited a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-registration a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-subscription a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .cs1-ws-icon a{background-size:contain;padding:0 1em 0 0}.mw-parser-output .cs1-code{color:inherit;background:inherit;border:none;padding:inherit}.mw-parser-output .cs1-hidden-error{display:none;color:var(--color-error,#bf3c2c)}.mw-parser-output .cs1-visible-error{color:var(--color-error,#bf3c2c)}.mw-parser-output .cs1-maint{display:none;color:#085;margin-left:0.3em}.mw-parser-output .cs1-kern-left{padding-left:0.2em}.mw-parser-output .cs1-kern-right{padding-right:0.2em}.mw-parser-output .citation .mw-selflink{font-weight:inherit}@media screen{.mw-parser-output .cs1-format{font-size:95%}html.skin-theme-clientpref-night .mw-parser-output .cs1-maint{color:#18911f}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .cs1-maint{color:#18911f}}ISBN 0-297-77960-5 is George Lascelles's autobiography.



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
  AssignClass (a95293ec-787a-4753-9832-3e310a090b7e)
 Call ID: a95293ec-787a-4753-9832-3e310a090b7e
  Args:
    source: George_Henry_Hubert_Lascelles
    type: :Man
  AssignClass (cbb43494-16e7-4515-b799-361bc4d111c1)
 Call ID: cbb43494-16e7-4515-b799-361bc4d111c1
  Args:
    source: George_Henry_Hubert_Lascelles
    type: :Person
  AddLiteral (4edb6164-1226-44b9-872d-1666d14d4634)
 Call ID: 4edb6164-1226-44b9-872d-1666d14d4634
  Args:
    literal_value: 1923
    source: George_Henry_Hubert_Lascelles
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (bb695729-3f37-4cc2-8d8d-362a867c4b9a)
 Call ID: bb695729-3f37-4cc2-8d8d-362a867c4b9a
  Args:
    relation: :hasDeathYear
    literal_value: 2011
    source: George_Henry_Hubert_Lascelles
    literal_type: xsd:integer
  AssignClass (7722eff6-a6bd-4c8d-aa70-c4210c80a013)
 Call ID: 7722eff6-a6bd-4c8d-aa70-c4210c80a013
  Args:
    type: :Man
    source: Henry_Viscount_Lascelles
  AssignClass (7e8a2d27-6c2e-4deb-9cd6-814a8d33381c)
 Call ID: 7e8a2d27-6c2e-4deb-9cd6-814a8d33381c
  Args:
    type: :Person
    source: Henry_Viscount_Lascelles
  AssignClass (1b333edf-f457-4e70-97ca-f02134186e40)
 Call ID: 1b333edf-f457-4e70-97ca-f02134186e40
  Args:
    source: Princess_Mary
    type: :Woman
  AssignClass (d559bf7c-391d-4f9b-bfca-8bfbb17e9331)
 Call ID: d559bf7c-391d-4f9b-bfca-8bfbb17e9331
  Args:
    type: :Person
    source: Princess_Mary
  AddTriple (dc78767c-9fa2-4a9e-837e-90d327ad535b)
 Call ID: dc78767c-9fa2-4a9e-837e-90d327ad535b
  Args:
    source: George_Henry_Hubert_Lascelles
    target: Henry_Viscount_Lascelles
    relation: :hasFather
  AddTriple (04cf6d45-a7aa-4342-8ab9-cb5a4fd4a23d)
 Call ID: 04cf6d45-a7aa-4342-8ab9-cb5a4fd4a23d
  Args:
    source: George_Henry_Hubert_Lascelles
    target: Princess_Mary
    relation: :hasMother
  AssignClass (87188e2b-f3f3-4cd5-a405-fa77c9437520)
 Call ID: 87188e2b-f3f3-4cd5-a405-fa77c9437520
  Args:
    source: King_George_V
    type: :Man
  AssignClass (fd73e751-2f06-4c76-b561-f2f2dba29c7d)
 Call ID: fd73e751-2f06-4c76-b561-f2f2dba29c7d
  Args:
    source: King_George_V
    type: :Person
  AssignClass (5fb830f4-7c25-448f-990f-0591bc254186)
 Call ID: 5fb830f4-7c25-448f-990f-0591bc254186
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (49ac85c0-0804-4380-90b6-45c7860f95b5)
 Call ID: 49ac85c0-0804-4380-90b6-45c7860f95b5
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (7f0d4c81-51f2-4eeb-85b0-24da742dcfe8)
 Call ID: 7f0d4c81-51f2-4eeb-85b0-24da742dcfe8
  Args:
    source: Princess_Mary
    target: King_George_V
    relation: :hasFather
  AddTriple (6035c658-7c38-4bde-97d5-18b4c280be6b)
 Call ID: 6035c658-7c38-4bde-97d5-18b4c280be6b
  Args:
    relation: :hasMother
    source: Princess_Mary
    target: Queen_Mary
  AssignClass (2cd4d2d7-8da4-4df7-b6bb-f608e51742aa)
 Call ID: 2cd4d2d7-8da4-4df7-b6bb-f608e51742aa
  Args:
    type: :Woman
    source: Marion_Stein
  AssignClass (cf18a729-537b-4a4b-bd57-c508bd16eecd)
 Call ID: cf18a729-537b-4a4b-bd57-c508bd16eecd
  Args:
    type: :Person
    source: Marion_Stein
  AssignClass (b5345da1-ffb9-4dbd-9bc4-524e49cfffd1)
 Call ID: b5345da1-ffb9-4dbd-9bc4-524e49cfffd1
  Args:
    source: Patricia_Bambi_Tuckwell
    type: :Woman
  AssignClass (88c2d714-b8e7-480a-a424-fac21c153467)
 Call ID: 88c2d714-b8e7-480a-a424-fac21c153467
  Args:
    type: :Person
    source: Patricia_Bambi_Tuckwell
  AddTriple (be5dda80-6334-4083-9eed-0b6639c89001)
 Call ID: be5dda80-6334-4083-9eed-0b6639c89001
  Args:
    source: George_Henry_Hubert_Lascelles
    target: Marion_Stein
    relation: :hasRelation
  AddLiteral (e85bcff5-9c88-42d7-8b8c-7c1c6f8f139f)
 Call ID: e85bcff5-9c88-42d7-8b8c-7c1c6f8f139f
  Args:
    literal_value: 1949
    source: George_Henry_Hubert_Lascelles
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (94d02ab5-6bda-4754-9fa4-34cc56feb0cf)
 Call ID: 94d02ab5-6bda-4754-9fa4-34cc56feb0cf
  Args:
    target: Patricia_Bambi_Tuckwell
    source: George_Henry_Hubert_Lascelles
    relation: :hasRelation
  AddLiteral (6a33ef58-7753-420b-9581-018e2e09e5be)
 Call ID: 6a33ef58-7753-420b-9581-018e2e09e5be
  Args:
    literal_value: 1967
    source: George_Henry_Hubert_Lascelles
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (65826390-6698-4768-b34d-02bb129d2b63)
 Call ID: 65826390-6698-4768-b34d-02bb129d2b63
  Args:
    type: :Man
    source: Mark_Lascelles
  AssignClass (c97fa960-3b41-4fdd-8025-ccf78e99436c)
 Call ID: c97fa960-3b41-4fdd-8025-ccf78e99436c
  Args:
    source: Mark_Lascelles
    type: :Person
  AddTriple (99eb8808-f05a-4872-b818-bbeef87c1fdf)
 Call ID: 99eb8808-f05a-4872-b818-bbeef87c1fdf
  Args:
    relation: :hasFather
    target: George_Henry_Hubert_Lascelles
    source: Mark_Lascelles
  AddTriple (246b0b79-270d-42c6-ae4c-c79104eb15ac)
 Call ID: 246b0b79-270d-42c6-ae4c-c79104eb15ac
  Args:
    target: Patricia_Bambi_Tuckwell
    source: Mark_Lascelles
    relation: :hasMother
  AssignClass (caed2d13-f300-4ba5-a868-afaf7249290b)
 Call ID: caed2d13-f300-4ba5-a868-afaf7249290b
  Args:
    source: Erwin_Stein
    type: :Man
  AssignClass (415914d3-902f-4f60-9593-dab81462cdfa)
 Call ID: 415914d3-902f-4f60-9593-dab81462cdfa
  Args:
    source: Erwin_Stein
    type: :Person
  AddTriple (5e36570e-3723-4f17-8fb5-73995549cba7)
 Call ID: 5e36570e-3723-4f17-8fb5-73995549cba7
  Args:
    source: Marion_Stein
    target: Erwin_Stein
    relation: :hasFather
  AssignClass (b67e04a5-4a58-42be-be6f-18caf27255b5)
 Call ID: b67e04a5-4a58-42be-be6f-18caf27255b5
  Args:
    source: Barry_Tuckwell
    type: :Man
  AssignClass (aae7e04a-cc89-4e18-9482-9d0f2c38ee73)
 Call ID: aae7e04a-cc89-4e18-9482-9d0f2c38ee73
  Args:
    source: Barry_Tuckwell
    type: :Person
  AddTriple (268f1eca-7153-41ce-8e3b-7c3d98e3c31e)
 Call ID: 268f1eca-7153-41ce-8e3b-7c3d98e3c31e
  Args:
    source: Patricia_Bambi_Tuckwell
    target: Barry_Tuckwell
    relation: :isSiblingOf
  Finish (e6417322-1d99-4c09-90bd-94906cb86427)
 Call ID: e6417322-1d99-4c09-90bd-94906cb86427
  Args: